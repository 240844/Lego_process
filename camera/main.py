import cv2
import skimage

import connector
import processing
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication
import interface
from classifier.lego_model import LegoBrickModel
from item_detector import paste_blobs, find_blobs, copy_identified_blobs, classify_blob, find_unclassified_blob, count_unclassified


def process(frame: np.ndarray, blobs: list):

    blurred_image = processing.gauss(frame, size=8)
    new_blobs = find_blobs(blurred_image)

    copy_identified_blobs(blobs, new_blobs)

    blob = find_unclassified_blob(new_blobs, frame.shape)
    if blob is not None:
        classify_blob(model, blob, frame)
        stats[blob.brick.name] = stats.get(blob.brick.name, 0) + 1

    print(stats)
    print(f"Classified {count_unclassified(new_blobs)}/{len(new_blobs)} blobs")

    image = paste_blobs(frame, new_blobs)
    return image, new_blobs


camera = connector.Connector(
    port=8080,
    width=540,
    height=960,
    fps=15
)

stats={}

model = LegoBrickModel('lego_classifier_model_[e=1,bs=50].keras')

app = QApplication(sys.argv)
gui = interface.Interface(camera, process, model)
gui.show()
sys.exit(app.exec_())
