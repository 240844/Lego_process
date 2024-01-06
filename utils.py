import os
import cv2


def get_root_dir():
    current_directory = os.getcwd()
    root_directory = os.path.abspath(os.path.join(current_directory, os.pardir))
    return root_directory

#zwraca obrazek w formacie RGB
def load_image(image_path, directory='data_processed'):
    image_path = os.path.join(get_root_dir(), directory, image_path)
    imageRGB = cv2.imread(image_path)[..., ::-1] # BGR -> RGB
    return imageRGB