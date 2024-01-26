import camera.connector as connector
import camera.interface as interface
import numpy as np
import sys
from app.utils.config import options
from PyQt5.QtWidgets import QApplication
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
                print(f"Classified {count_unclassified(new_blobs)}/{len(new_blobs)} blobs")

    #stats_string = stats_to_string()
    #print(stats_string)
    #print(f"Classified {count_unclassified(new_blobs)}/{len(new_blobs)} blobs")

    image = paste_blobs(frame, new_blobs)
    return image, new_blobs


camera = connector.Connector(
    port=options.port,
    width=options.width,
    height=options.height,
    fps_max=options.fps
)


model = LegoBrickModel('lego_classifier_model_test_split_adam_[e=5,bs=600]' + '.keras')

app = QApplication(sys.argv)
gui = interface.Interface(camera, process, model)
gui.show()
sys.exit(app.exec_())
