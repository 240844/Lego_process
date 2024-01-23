import time
import numpy as np
import cv2
from PyQt5.QtCore import pyqtSignal, QThread

"""
http://192.168.0.4:8080/
"""


class Connector(QThread):
    frame_signal = pyqtSignal(np.ndarray)
    default_ip = "http://192.168.173.194"

    def __init__(self, ip=default_ip, port=8080, width=540, height=960, fps_max=30):
        super().__init__()
        self.ip = ip
        self.port = port
        self.width = width
        self.height = height
        self.fps = fps_max
        self.is_running = False

    def run(self):
        self.is_running = True
        time_diff = 0
        capture = cv2.VideoCapture(f"{self.ip}:{self.port}/video")
        if not capture.isOpened():
            print("#### Capture stream cannot be opened.")
        while capture.isOpened() and self.is_running:
            time_elapse = time.time() - time_diff
            ret, frame = capture.read()

            if time_elapse < 1. / self.fps:
                continue
            try:
                time_diff = time.time()
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
