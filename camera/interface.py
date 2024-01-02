from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np


class Interface(QWidget):
    def __init__(self, connector):
        super().__init__()
        self.connector = connector

        self.setWindowTitle("Qt live label demo")
        self.disply_width = 640
        self.display_height = 480
        # create the label that holds the image
        self.image_label = QLabel(self)
        self.image_label.resize(self.disply_width, self.display_height)
        # create a text label
        self.textLabel = QLabel('Webcam')

        # create a vertical box layout and add the two labels
        vbox = QVBoxLayout()
        vbox.addWidget(self.image_label)
        vbox.addWidget(self.textLabel)
        # set the vbox layout as the widgets layout
        self.setLayout(vbox)

        # create the video capture thread
        # self.thread = VideoThread()
        # connect its signal to the update_image slot
        self.connector.frame_signal.connect(self.update_image)
        # start the thread
        self.connector.start()

    def closeEvent(self, event):
        self.connector.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def update_image(self, cv_img):
        """Updates the image_label with a new opencv image"""
        rgb_image = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
        h, w, ch = rgb_image.shape
        bytes_per_line = ch * w
        convert_to_Qt_format = QtGui.QImage(rgb_image.data, w, h, bytes_per_line, QtGui.QImage.Format_RGB888)
        p = convert_to_Qt_format.scaled(self.disply_width, self.display_height, Qt.KeepAspectRatio)
        qt_img = QPixmap.fromImage(p)
        self.image_label.setPixmap(qt_img)
