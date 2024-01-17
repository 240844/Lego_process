from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np
import random


class Interface(QWidget):
    def __init__(self, camera, proces, model):
        super().__init__()
        self.setWindowTitle("lego_process")
        self.camera = camera
        self.process = proces
        self.model = model
        self.image = QLabel(self)
        self.title = "Predictions"
        self.test_predictions = ""
        self.text = QLabel(self.title)

        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(self.image)
        vbox.addWidget(self.text)
        vbox.setAlignment(Qt.AlignTop)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        self.camera.frame_signal.connect(self.update_image)
        self.camera.start()

    def closeEvent(self, event):
        self.camera.stop()
        event.accept()

    def predictions_to_text(self, processed_image):
        title = self.title
        if self.model is None:
            title = "Test " + title
            prediction_text = "\n".join([f"var {i}: {str(random.randint(0, 100))}%" for i in range(0, 10)])
        else:
            predict = self.model.predict(processed_image)
            prediction_text = "\n".join([str(entry) for entry in predict])
        self.text.setText(title + "\n" + prediction_text)

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        try:
            processed_image = self.process(cv_img)
            self.predictions_to_text(processed_image)

            rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            qt_image = QtGui.QImage(rgb_image.data, w, w, ch * w, QtGui.QImage.Format_RGB888)
            #qt_image = QtGui.QImage(rgb_image.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
            pixmap_image = QPixmap.fromImage(qt_image)
            self.image.setPixmap(pixmap_image)
        except Exception as e:
            print("#### Image cannot be updated.")
            print(e)
            exit(1)
