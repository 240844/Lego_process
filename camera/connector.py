import subprocess
import time

import cv2

"""
http://192.168.0.4:8080/
"""


class Connector:
    def __init__(self, port=8080, width=540, height=960, fps=30):
        self.port = port
        self.width = width
        self.height = height
        self.fps = fps

    def run(self, processing):
        time_diff = 0
        capture = cv2.VideoCapture(f"https://192.168.0.4:{self.port}/video")
        if not capture.isOpened():
            print("#### Capture stream cannot be opened.")
        while capture.isOpened():
            ret, frame = capture.read()
            time_elapse = time.time() - time_diff
            if time_elapse < 1./self.fps:
                continue
            try:
                time_diff = time.time()
                frame = cv2.resize(frame, (self.width, self.height))
                frame = processing(frame)
                cv2.imshow("temp", frame)
                if cv2.waitKey(1) & 0xFF == ord('c'):
                    break
            except cv2.error as e:
                print("#### Stream has been closed.")
                print(e)
                break

        capture.release()
        cv2.destroyAllWindows()
