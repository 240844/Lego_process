import connector
import processing
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication
import interface


def process(frame: np.ndarray):
    v = frame.copy()
    v = processing.grey_scale(v)
    v = processing.gauss(v, size=4)
    """
    Canny edges detection
    """
    v = processing.canny(v, t1=200, t2=255)
    v = processing.dilation(v, size=6)

    return v


camera = connector.Connector(
    port=8080,
    width=540,
    height=960,
    fps=10
)

model = None

app = QApplication(sys.argv)
gui = interface.Interface(camera, process, model)
gui.show()
sys.exit(app.exec_())
