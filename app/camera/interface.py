import time

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
import random

# TODO Zrobić obsługę alarmu gdy p-stwo predykcji nie przekracza
#  thresholdu
# zrobić nasłuchiwanie klawiatury Q/Start
# zrobić okno wprowadzania IP

def crop_into_square(cv_img):
    size = cv_img.shape[1]
    return cv_img[0:size, 0:size]


class Interface(QWidget):
    def __init__(self, camera, proces, model):
        super().__init__()
        self.time = time.time()
        self.fps = 0
        self.setWindowTitle("lego_process")
        self.camera = camera
        self.process = proces
        self.blobs = []
        self.stats = {}
        self.title = "Lego stats:"
        self.model = model
        self.image = QLabel(self)
        self.test_predictions = ""
        self.stats_text = QLabel(self.title)
        self.reset_stats_button = QPushButton('Reset stats', self)
        self.frame_counter = 0

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(self.image)
        vbox.addWidget(self.reset_stats_button)
        self.reset_stats_button.clicked.connect(self.reset_stats)
        vbox.addWidget(self.stats_text)
        vbox.setAlignment(Qt.AlignTop)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        self.camera.frame_signal.connect(self.update_image)
        self.camera.start()

    def reset_stats(self):
        self.stats = {}
        self.stats_text.setText(self.title)
        for blob in self.blobs:
            blob.brick = None
            blob.confidence = None

    def closeEvent(self, event):
        self.camera.stop()
        event.accept()

    def view_stats(self):
        if self.model is not None:
            stats_text = self.stats_to_string()
        else:
            stats_text = "No model loaded"

        self.stats_text.setText(self.title + "\n" + stats_text)

    def stats_to_string(self):
        stats_string = ""
        for key, value in self.stats.items():
            stats_string += f"{key}: {value}\n"
        return stats_string

    def update_fps(self):
        self.frame_counter += 1
        if self.frame_counter % 10 == 0:
            self.fps = 10 / (time.time() - self.time)
            self.time = time.time()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        cv_img = crop_into_square(cv_img)
        try:
            self.update_fps()
            processed_image, self.blobs = self.process(cv_img, self.blobs, self.stats)
            processed_image = cv2.putText(processed_image, str(f"{int(self.fps)} fps"), (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)

            rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            qt_image = QtGui.QImage(rgb_image.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
            pixmap_image = QPixmap.fromImage(qt_image)
            self.image.setPixmap(pixmap_image)
            self.view_stats()

        except Exception as e:
            print("#### Image cannot be updated.")
            print(e)
            exit(1)
