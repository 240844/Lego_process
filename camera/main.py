import connector
import processing
import numpy as np


def process(frame: np.ndarray):
    v = frame.copy()
    v = processing.grey_scale(v)
    v = processing.gauss(v, size=4)
    """
    Canny edges detection
    """
    v = processing.canny(v, t1=100, t2=200)
    v = processing.dilation(v, size=6)
    #v = processing.paint_label(frame, v)
    return v


camera = connector.Connector()
camera.run(process)
