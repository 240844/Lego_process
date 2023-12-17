import cv2
import skimage as ski
import numpy as np


def grey_scale(frame: np.ndarray) -> np.ndarray:
    processed_frame = ski.color.rgb2gray(frame)
    return processed_frame


def thresholding(frame: np.ndarray, threshold=0.5) -> np.ndarray:
    ret, bin_img = cv2.threshold(frame, threshold, 1, cv2.THRESH_BINARY)
    return bin_img


def gauss(frame: np.ndarray, size=5):
    kernel = np.ones((size, size), np.float32) / size ** 2
    frame_gauss = cv2.filter2D(frame, -1, kernel)
    return frame_gauss


def canny(frame: np.ndarray, t1=100, t2=200) -> np.ndarray:
    frame_canny = cv2.Canny(np.uint8(255 * frame), t1, t2)
    return frame_canny
