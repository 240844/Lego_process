import subprocess
import time
import numpy as np
import cv2
from PyQt5.QtCore import pyqtSignal, QThread

"""
http://192.168.0.4:8080/
"""

default_ip = "https://192.168.0.4"


class Connector(QThread):
    frame_signal = pyqtSignal(np.ndarray)
    parameters_signal = pyqtSignal(list)

    def __init__(self, processing, port=8080, width=540, height=960, fps=30):
        super().__init__()
        self.processing = processing
        self.port = port
        self.width = width
        self.height = height
        self.fps = fps
        self.is_running = False


    def run(self):
        self.is_running = True
        time_diff = 0
        capture = cv2.VideoCapture(f"{default_ip}:{self.port}/video")
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
                frame = self.processing(frame)
                self.frame_signal.emit(frame)
                # self.parameters_signal.emit(frame)
                # cv2.imshow("temp", frame)
                # if cv2.waitKey(1) & 0xFF == ord('c'):
                #     break
            except cv2.error as e:
                print(e)
                break
        print("#### Stream has been closed.")
        capture.release()
        cv2.destroyAllWindows()

    def close(self):
        self.is_running = False
