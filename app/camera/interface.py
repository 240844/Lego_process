import time
from app.camera.connector import Connector
from app.utils.config import options
from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout, QVBoxLayout, QPushButton, QInputDialog, QSizePolicy, QLineEdit
from PyQt5.QtGui import QPixmap
import cv2
from PyQt5.QtCore import pyqtSlot, Qt
import numpy as np


class Interface(QWidget):
    def __init__(self, camera: Connector, proces, model):
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
        self.alarm_label = QLabel("Alarm! Unwanted objects!")
        self.reset_stats_button = QPushButton('Reset stats', self)
        self.reset_stats_button.clicked.connect(self.resetStats)

        self.pause_button = QPushButton('Pause', self)
        self.pause_button.clicked.connect(self.togglePause)

        self.frame_counter = 0
        self.alarm = False
        policy = QSizePolicy()
        policy.setRetainSizeWhenHidden(True)

        # Create layout
        hbox = QHBoxLayout()
        vbox = QVBoxLayout()
        hbox.addWidget(self.image)
        vbox.addWidget(self.alarm_label)
        self.alarm_label.setSizePolicy(policy)
        vbox.addWidget(self.reset_stats_button)
        vbox.addWidget(self.pause_button)
        vbox.addWidget(self.stats_text)
        vbox.setAlignment(Qt.AlignTop)
        hbox.addLayout(vbox)
        self.setLayout(hbox)

        # Get IP from user
        ip, ok = QInputDialog.getText(self, 'lego-object-detection', 'Input camera-device IP', text=options.ip)
        if ok:
            camera.set_ip(ip)
            options.ip = ip
            options.saveConfig()

        # Connect with camera
        self.camera.frame_signal.connect(self.updateImage)
        self.camera.start()

    # On close event handling.
    def closeEvent(self, event):
        self.camera.close()
        event.accept()

    # Reset blobs and labels service.
    def resetStats(self):
        self.stats = {}
        self.stats_text.setText(self.title)
        for blob in self.blobs:
            blob.brick = None
            blob.confidence = None

    def togglePause(self):
        if self.pause_button.text() == "Pause":
            self.pause_button.setText("Resume")
            self.camera.close()
        else:
            self.pause_button.setText("Pause")
            self.camera.start()

    def handleAlarm(self):
        self.alarm_label.setVisible(self.alarm)
        if not self.alarm:
            return
        if self.frame_counter < options.frames_per_sample:
            self.alarm_label.setStyleSheet("QLabel { background-color : red; color : white; }")
        else:
            self.alarm_label.setStyleSheet("QLabel { background-color : white; color : red; }")

    # Update object classification labels.
    def updateLabels(self):
        self.alarm = False
        if self.model is None:
            stats_string = "No model loaded"
        else:
            stats_string = ""
            for key, value in self.stats.items():
                stats_string += f"{key}: {value}\n"
        self.stats_text.setText(self.title + "\n" + stats_string)

    # Update frames per second label.
    def updateFps(self, processed_image):
        self.frame_counter = (self.frame_counter + 1) % (2 * options.frames_per_sample)
        if self.frame_counter % (2 * options.frames_per_sample) == 0:
            self.fps = (2 * options.frames_per_sample) / (time.time() - self.time)
            self.time = time.time()
        image = cv2.putText(processed_image, str(f"{int(self.fps)} fps"), (5, 20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255, 255, 255), 1, cv2.LINE_AA)
        return image

    # Update rectangles around objects.
    def updateBlobs(self, image):
        image = image.copy()

        for blob in self.blobs:
            brick = blob.brick

            if blob.unwanted:
                self.alarm = True
                name = "Unwanted"
                confidence = ""
                color = (255, 255 * self.frame_counter / options.frames_per_sample, 0)
            elif brick is None:
                name = "Not classified"
                confidence = ""
                color = (255, 255, 255)

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
    def updateImage(self, cv_img):
        cv_img = cv_img[0:cv_img.shape[1], 0:cv_img.shape[1]]
        try:
            classify = self.frame_counter % options.frames_per_sample == 0
            processed_image, self.blobs, self.stats = self.process(cv_img, self.blobs, self.stats, classify)
            processed_image = self.updateBlobs(processed_image)
            processed_image = self.updateFps(processed_image)

            rgb_image = cv2.cvtColor(processed_image, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            qt_image = QtGui.QImage(rgb_image.data, w, h, ch * w, QtGui.QImage.Format_RGB888)
            pixmap_image = QPixmap.fromImage(qt_image)
            self.image.setPixmap(pixmap_image)
            self.handleAlarm()
            self.updateLabels()

        except Exception as e:
            print("#### Image cannot be updated.")
            print(e)
            exit(1)
