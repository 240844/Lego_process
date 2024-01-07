import os
import cv2
import numpy as np


def decrease_resolution(image: np.ndarray, step: int = 10) -> np.ndarray:
    image = image[::step, ::step]
    return image


def threshold(gray_image: np.ndarray) -> np.ndarray:
    ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh


def get_avg(image: np.ndarray) -> list:
    output1 = np.average(image[:, :, 0])
    output2 = np.average(image[:, :, 1])
    output3 = np.average(image[:, :, 2])
    output = [output1, output2, output3]
    return output


def rgb_to_grayscale(image: np.ndarray) -> np.ndarray:
    b, g, r = cv2.split(image)
    grayscale_image = 0.299 * r + 0.587 * g + 0.114 * b
    grayscale_image = np.uint8(grayscale_image)
    return grayscale_image


def reduce(image: np.ndarray, num_colors: int = 2) -> np.ndarray:
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)
    return segmented_image


def get_darkest_color(image: np.ndarray):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    min_intensity_coord = np.unravel_index(np.argmin(gray_img), gray_img.shape)
    darkest_color = image[min_intensity_coord]
    return darkest_color


def replace_color(image: np.ndarray, old_background_color: np.ndarray, new_background_color) -> np.ndarray:
    new_image = image.copy()
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if np.all(image[x, y] == old_background_color):
                new_image[x, y] = new_background_color
    return new_image


def save_img(image: np.ndarray, directory: str, filename: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

    full_path = os.path.join(directory, filename)

    cv2.imwrite(full_path, image)
    return None


def make_new_dir(new_dir: str) -> None:
    current_dir = os.getcwd()
    file_list = os.listdir()
    if new_dir not in file_list:
        os.mkdir(new_dir)
    os.chdir(current_dir)
    return None
