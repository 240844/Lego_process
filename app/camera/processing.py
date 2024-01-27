import cv2
import skimage as ski
import numpy as np


def grey_scale(frame: np.ndarray) -> np.ndarray:
    gray_frame = frame.copy()
    return cv2.cvtColor(gray_frame, cv2.COLOR_BGR2GRAY)


def gauss(frame: np.ndarray, size=5):
    kernel = np.ones((size, size), np.float32) / size ** 2
    frame_gauss = cv2.filter2D(frame, -1, kernel)
    return frame_gauss


def canny(frame: np.ndarray, t1=100, t2=200) -> np.ndarray:
    frame_canny = cv2.Canny(np.uint8(255 * frame), t1, t2)
    return frame_canny


def dilation(frame, size=5):
    kernel = np.ones((size, size), np.uint8)
    frame_dilation = cv2.dilate(frame, kernel, iterations=1)
    return frame_dilation


def region_props(frame):
    labels = ski.measure.label(frame)
    frame_regions = ski.measure.regionprops(labels)
    for region in frame_regions:
        minr, minc, maxr, maxc = region.bbox
        rr, cc = ski.draw.rectangle(start=(minr, minc), end=(maxr, maxc), extent=None, shape=frame.shape)
        frame[rr, cc] = 255
    return ski.util.img_as_ubyte(frame)
