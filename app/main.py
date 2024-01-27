import camera.connector as connector
import camera.processing as processing
import camera.interface as interface
import numpy as np
import sys
from app.utils.config import options
from PyQt5.QtWidgets import QApplication
from app.classifier.lego_model import LegoBrickModel
from app.detector.item_detector import find_blobs, copy_identified_blobs, classify_blob, \
    find_unclassified_blob, count_unclassified


# Create process pipeline
def process(frame: np.ndarray, blobs: list, labels: dict, classify=True):
    new_blobs = find_blobs(frame)

    copy_identified_blobs(blobs, new_blobs)
    if classify:
        blob = find_unclassified_blob(new_blobs, frame.shape)
        if blob is not None:
            classify_blob(model, blob, frame)
            labels[blob.brick.name] = labels.get(blob.brick.name, 0) + 1
            print(f"Classified {count_unclassified(new_blobs)}/{len(new_blobs)} blobs")



    return frame, new_blobs, labels


camera = connector.Connector(
    port=options.port,
    width=options.width,
    height=options.height
)


model = LegoBrickModel('lego_classifier_adam_[e=5,bs=600]' + '.keras')

app = QApplication(sys.argv)
gui = interface.Interface(camera, process, model)
gui.show()
sys.exit(app.exec_())
