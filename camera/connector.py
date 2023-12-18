import subprocess

import cv2

"""
http://192.168.0.4:8080/
"""


class Connector:
    def __init__(self, port=8080, width=540, height=960):
        self.port = port
        self.width = width
        self.height = height

    def run(self, processing):
        capture = cv2.VideoCapture(f"https://192.168.0.4:{self.port}/video")
        if not capture.isOpened():
            print("#### Capture stream cannot be opened.")
        while capture.isOpened():
            ret, frame = capture.read()
            try:
                frame = processing(frame)
                cv2.imshow("temp", cv2.resize(frame, (self.width, self.height)))
                if cv2.waitKey(20) & 0xFF == ord('c'):
                    break
            except cv2.error as e:
                print("#### Stream has been closed.")
                print(e)
                break

        capture.release()
        cv2.destroyAllWindows()
