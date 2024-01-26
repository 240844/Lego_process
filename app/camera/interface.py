import time

from app.utils.config import options
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QInputDialog
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np


class Interface(QWidget):
    def __init__(self, camera, proces, model):
        # Init variables
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

        # Create layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(self.image)
        vbox.addWidget(self.reset_stats_button)
        self.reset_stats_button.clicked.connect(self.reset_stats)
        vbox.addWidget(self.stats_text)
        vbox.setAlignment(Qt.AlignTop)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        # Get IP from user
        ip, ok = QInputDialog.getText(self, 'lego-object-detection', 'Input camera-device IP', text=options.ip)
        if ok:
            camera.set_ip(ip)

        # Connect with camera
        self.camera.frame_signal.connect(self.update_image)
        self.camera.start()

    # On close event handling.
    def closeEvent(self, event):
        self.camera.stop()
        event.accept()

    # Reset blobs and labels service.
    def reset_stats(self):
        self.stats = {}
        self.stats_text.setText(self.title)
        for blob in self.blobs:
            blob.brick = None
            blob.confidence = None

    # Update object classification labels.
    def update_labels(self):
        if self.model is not None:
            stats_string = ""
            for key, value in self.stats.items():
                stats_string += f"{key}: {value}\n"
        else:
            stats_string = "No model loaded"
        self.stats_text.setText(self.title + "\n" + stats_string)

    # Update frames per second label.
    def update_fps(self, processed_image):
        self.frame_counter += 1
        if self.frame_counter % 10 == 0:
            self.fps = 10 / (time.time() - self.time)
            self.time = time.time()
        image = cv2.putText(processed_image, str(f"{int(self.fps)} fps"), (5, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        return image

    # Update rectangles around objects.
    def update_blobs(self, image):
        image = image.copy()

        for blob in self.blobs:
            brick = blob.brick

            if brick is None:
                color = (255, 255, 255)
                name = "Not classified"
                confidence = ""
            else:
                color = brick.getColor()
                name = brick.name
                confidence = f"{blob.confidence:.2f}"

            cv2.rectangle(image, (blob.x, blob.y), (blob.x + blob.w, blob.y + blob.h), color, thickness=2)
            cv2.putText(image, str(name), (blob.x + blob.w + 10, blob.y + 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color,
                        thickness=1)
            cv2.putText(image, str(confidence), (blob.x + blob.w + 10, blob.y + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                        color, thickness=1)

        return image

    # Update image view in UI window.
    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        cv_img = self.crop_into_square(cv_img)
        try:
            classify = self.frame_counter % 5 == 0
            processed_image, self.blobs = self.process(cv_img, self.blobs, self.stats, classify)
            processed_image = self.update_blobs(processed_image)
            processed_image = self.update_fps(processed_image)

            rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            qt_image = QtGui.QImage(rgb_image.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
            pixmap_image = QPixmap.fromImage(qt_image)
            self.image.setPixmap(pixmap_image)
            self.update_labels()

        except Exception as e:
            print("#### Image cannot be updated.")
            print(e)
            exit(1)

    @staticmethod
    def crop_into_square(cv_img):
        size = cv_img.shape[1]
        return cv_img[0:size, 0:size]
