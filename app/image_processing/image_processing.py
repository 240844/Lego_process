import os

import cv2
import numpy as np

from utils import save_img, replace_color, get_darkest_color, reduce, decrease_resolution, get_avg


def square(img, a=56):

    height, width = img.shape[:2]
    if height > width:
        scale_factor = a / height
    else:
        scale_factor = a / width

    resized_img = cv2.resize(img, None, fx=scale_factor, fy=scale_factor)
    black_img = np.zeros((a, a, 3), np.uint8)
    x_offset = int((black_img.shape[0] - resized_img.shape[0]) / 2)
    y_offset = int((black_img.shape[1] - resized_img.shape[1]) / 2)
    black_img[x_offset:resized_img.shape[0] + x_offset, y_offset:resized_img.shape[1] + y_offset] = resized_img

    return black_img

def rotate_image(image: np.ndarray, angle: int) -> np.ndarray:
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    img_avg = get_avg(result)
    for x in range(result.shape[0]):
        for y in range(result.shape[1]):
            if np.array_equal([0, 0, 0], result[x, y]):
                result[x, y] = np.asarray(img_avg)
    return result


def zoom_out(image: np.ndarray, scale: int = 50) -> np.ndarray:
    new_image = np.zeros_like(image)
    width = int(image.shape[1] * scale / 100)
    height = int(image.shape[0] * scale / 100)
    small_image = cv2.resize(image, (width, height))
    x_margin= int((image.shape[0] - small_image.shape[0]) / 2)
    y_margin = int((image.shape[1] - small_image.shape[1]) / 2)
    new_image[x_margin:small_image.shape[0] + x_margin, y_margin:small_image.shape[1] + y_margin] = small_image

    return new_image


def zoom_in(image: np.ndarray, scale: int = 50) -> np.ndarray:
    x_offset = int(image.shape[0] / 4)
    y_offset = int(image.shape[1] / 4)
    n_width = image.shape[0]
    n_height = image.shape[1]
    new_image = np.zeros((n_width, n_height, 3))
    scale += 100
    width = int(image.shape[1] * scale / 100)
    height = int(image.shape[0] * scale / 100)
    dim = (width, height)
    img = cv2.resize(image, dim)
    for x in range(n_width):
        for y in range(n_height):
            new_image[x, y] = img[x + x_offset, y + y_offset]
    return new_image


class ImageProcessor:

    def __init__(self):
        self.folders = {}
        self.directory_path = ""

    def load_images(self, path: str) -> None:
        self.folders = {}
        self.directory_path = path

        for folder_name in os.listdir(path):
            images = []
            folder_name_ = f'{path}/{folder_name}'
            for name in os.listdir(folder_name_):
                name = f'{folder_name_}/{name}'
                image = cv2.imread(name)
                images.append(image)
            self.folders.update({folder_name: images})

        self.print_status()
        return None

    def mirror(self) -> None:
        print("mirroring...")

        for folder_name in self.folders:
            print("\tmirroring ",folder_name)
            images = self.folders[folder_name]
            images_flipped = []

            for image in images:
                images_flipped.append(cv2.flip(image, 1))

            images.extend(images_flipped)

        return None

    def print_status(self) -> None:
        print("status:")
        for folder_name in self.folders:
            print(folder_name, "-", len(self.folders[folder_name]), "images")

        return None

    def save(self) -> None:
        print("saving...")

        for folder_name in self.folders:
            print("\tsaving ",folder_name)
            for i, image in enumerate(self.folders[folder_name]):
                cdir = os.getcwd()

                dir_ = cdir + "\\" + self.directory_path + "_processed\\" + folder_name
                filename = folder_name + "_" + str(i) + ".png"

                #print(dir + "\\" + filename)
                save_img(image, dir_, filename)

        print("saved")
        return None

    def replace_darkest_color(self, new_color: tuple[int, int, int] = (0, 0, 0)) -> None:
        folders_edited = {}
        print("replacing darkest color...")

        for folder_name in self.folders:
            print("\treplacing ",folder_name)
            images = self.folders[folder_name]

            images_edited = []
            for image in images:
                old_background_color = get_darkest_color(image)
                edited_image = replace_color(image, old_background_color, new_color)
                images_edited.append(edited_image)

            folders_edited.update({folder_name: images_edited})
            images.extend(images_edited)

        self.folders = folders_edited
        return None

    def reduce_colors(self, color_amount: int = 2) -> None:
        print("reducing colors...")
        folders_edited = {}

        for folder_name in self.folders:
            print("\treducing ",folder_name)
            images = self.folders[folder_name]

            images_edited = []
            for image in images:
                images_edited.append(reduce(image, color_amount))

            folders_edited.update({folder_name: images_edited})
            images.extend(images_edited)

        self.folders = folders_edited
        return None

    def decrease_resolutions(self, param: int) -> None:
        print("decreasing resolution...")
        folders_edited = {}
        for folder_name in self.folders:
            images = self.folders[folder_name]

            images_edited = []
            for image in images:
                images_edited.append(decrease_resolution(image, param))

            folders_edited.update({folder_name: images_edited})
            images.extend(images_edited)

        self.folders = folders_edited
        return None

    def rotate_images(self, angle: int = 20) -> None:
        rotations = 360 // angle
        print("rotating...")
        for folder_name in self.folders:
            print("\trotating ",folder_name)
            images = self.folders[folder_name]
            images_rotated = []

            for image in images:
                for i in range(rotations):
                    images_rotated.append(rotate_image(image, angle*i))

            images.extend(images_rotated)

        self.print_status()
        return None

    def zoom_all(self) -> None:
        print("zooming...")
        for folder_name in self.folders:
            print("\tzooming ",folder_name)
            images = self.folders[folder_name]
            images_zoomed = []
            for image in images:
                images_zoomed.append(zoom_out(image, scale=50))
                images_zoomed.append(zoom_out(image, scale=25))
                images_zoomed.append(zoom_in(image, scale=50))
                images_zoomed.append(zoom_in(image, scale=25))
            images.extend(images_zoomed)
        self.print_status()
        return None

    def change_color(self) -> None:
        print("changing color...")
        for folder_name in self.folders:
            print("\tchanging color ",folder_name)
            images = self.folders[folder_name]
            new_images = []
            for image in images:
                new_images.append(cv2.convertScaleAbs(image, alpha=1, beta=10))
                new_images.append(cv2.convertScaleAbs(image, alpha=-1, beta=5))
            images.extend(new_images)
        self.print_status()
        return None



