import numpy as np
import cv2
from PyQt5.QtCore import pyqtSignal, QThread

"""
http://192.168.0.4:8080/
"""


# Class used to connect application with camera hosted in the same local network.
class Connector(QThread):
    frame_signal = pyqtSignal(np.ndarray)
    default_ip = "192.168.0.4"

    def __init__(self, ip=default_ip, port=8080, width=540, height=960):
        super().__init__()
        self.ip = ip
        self.port = port
        self.width = width
        self.height = height
        self.is_running = False

    # Method setting IP using to load IP from configuration file.
    def set_ip(self, ip: str):
        self.ip = ip

    # Main thread
    def run(self):
        # Configure video capture
        self.is_running = True
        capture = cv2.VideoCapture(f"http://{self.ip}:{self.port}/video")

        if not capture.isOpened():
            print("#### Capture stream cannot be opened.")
        while capture.isOpened() and self.is_running:
            ret, frame = capture.read()

            try:
                frame = cv2.resize(frame, (self.width, self.height))
                self.frame_signal.emit(frame)
            except cv2.error as e:
                print("#### Stream cannot be emitted.")
                print(e)
                break
        print("#### Stream has been closed.")
        capture.release()

    def close(self):
        self.is_running = False
