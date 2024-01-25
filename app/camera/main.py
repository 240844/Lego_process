import connector
import processing
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication
import interface
from app.classifier.lego_model import LegoBrickModel
from app.detector.item_detector import paste_blobs, find_blobs, copy_identified_blobs, classify_blob, find_unclassified_blob, count_unclassified


def process(frame: np.ndarray, blobs: list, stats: dict, classify=True):

    new_blobs = find_blobs(frame)

    copy_identified_blobs(blobs, new_blobs)
    if classify:
        blob = find_unclassified_blob(new_blobs, frame.shape)
        if blob is not None:
            valid = classify_blob(model, blob, frame)
            if valid:
                stats[blob.brick.name] = stats.get(blob.brick.name, 0) + 1

    #stats_string = stats_to_string()
    #print(stats_string)
    print(f"Classified {count_unclassified(new_blobs)}/{len(new_blobs)} blobs")

    image = paste_blobs(frame, new_blobs)
    return image, new_blobs


camera = connector.Connector(
    port=8080,
    width=540,
    height=960,
    fps_max=30
)


model = LegoBrickModel('lego_classifier_model_None_[e=1,bs=600]' + '.keras')

app = QApplication(sys.argv)
gui = interface.Interface(camera, process, model)
gui.show()
sys.exit(app.exec_())
