from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5.QtCore import pyqtSlot
import numpy as np


class Interface(QWidget):
    def __init__(self, camera, proces, model):
        super().__init__()
        self.setWindowTitle("lego_process")
        self.camera = camera
        self.process = proces
        self.model = model
        self.image = QLabel(self)
        self.text = QLabel("Predictions")

        hbox = QHBoxLayout()
        hbox.addWidget(self.image)
        hbox.addWidget(self.text)

        self.setLayout(hbox)

        self.camera.frame_signal.connect(self.update_image)
        self.camera.start()

    def closeEvent(self, event):
        self.camera.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        try:
            processed_image = self.process(cv_img)

            if self.model is not None:
                self.text = self.model.predict(processed_image)
            else:
                self.text = processed_image.shape

            rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            qt_image = QtGui.QImage(rgb_image.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
            pixmap_image = QPixmap.fromImage(qt_image)
            self.image.setPixmap(pixmap_image)
        except Exception as e:
            print("#### Image cannot be updated.")
            print(e)
            exit(1)

