import connector
import processing
import numpy as np


def process(frame: np.ndarray):
    v = frame.copy()
    v = processing.grey_scale(v)
    v = processing.gauss(v, 4)
    v = processing.canny(v, 100, 200)
    return v


camera = connector.Connector()
camera.run(process)
