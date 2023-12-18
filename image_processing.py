import cv2
import os

import numpy as np


def decrease_resolution(img, step=10):
    img = img[::step, ::step]
    return img

def treshold(gray_image):
    ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh


def rgb_to_grayscale(image, method=2):
    b, g, r = cv2.split(image)
    if method == 1:
        grayscale_image = (r + g + b) / 3
        return np.uint8(grayscale_image)
    elif method == 2:
        grayscale_image = 0.299 * r + 0.587 * g + 0.114 * b
        return np.uint8(grayscale_image)
    elif method == 3:
        grayscale_image = 0.3 * r + 0.4 * g + 0.3 * b
        return np.uint8(grayscale_image)


def get_avg(img):
    output1 = np.average(img[:, :, 0])
    output2 = np.average(img[:, :, 1])
    output3 = np.average(img[:, :, 2])
    output = [output1, output2, output3]
    return output

def reduce(image, num_colors=2):
    pixels = image.reshape((-1, 3))
    pixels = np.float32(pixels)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)
    _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)
    centers = np.uint8(centers)
    segmented_image = centers[labels.flatten()]
    segmented_image = segmented_image.reshape(image.shape)
    return segmented_image


def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    img_avg = get_avg(result)
    for x in range(result.shape[0]):
        for y in range(result.shape[1]):
            if np.array_equal([0, 0, 0], result[x, y]):
                result[x, y] = np.asarray(img_avg)
    return result

def get_darkest_color(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    min_intensity_coord = np.unravel_index(np.argmin(gray_img), gray_img.shape)
    darkest_color = image[min_intensity_coord]
    return darkest_color


def replace_color(image, old_background_color, new_background_color):

    new_image = image.copy()
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if np.all(image[x, y] == old_background_color):
                new_image[x, y] = new_background_color

    return new_image


class ImageProcessor:


    def __init__(self):
        self.folders = {}
        self.directory_path = ""

    def load_images(self, path: str):
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

    def mirror(self) -> None:

        for folder_name in self.folders:
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

    def save(self, path: str) -> None:
        print("saving...")

        for folder_name in self.folders:
            for i, image in enumerate(self.folders[folder_name]):
                cdir = os.getcwd()

                dir = cdir + "\\" + self.directory_path + "_processed\\" + folder_name
                filename = folder_name + "_" + str(i) + ".png"

                #print(dir + "\\" + filename)
                save_img(image, dir, filename)

        print("saved")
        return None


    def replace_darkest_color(self, new_color=(0,0,0)):
        folders_edited = {}

        for folder_name in self.folders:
            images = self.folders[folder_name]

            images_edited = []
            for image in images:
                old_background_color = get_darkest_color(image)
                edited_image = replace_color(image, old_background_color,new_color)
                images_edited.append(edited_image)

            folders_edited.update({folder_name: images_edited})
            images.extend(images_edited)

        self.folders = folders_edited
        return None

    def reduce_colors(self, color_amount=2):
        folders_edited = {}

        for folder_name in self.folders:
            images = self.folders[folder_name]

            images_edited = []
            for image in images:
                images_edited.append(reduce(image, color_amount))

            folders_edited.update({folder_name: images_edited})
            images.extend(images_edited)

        self.folders = folders_edited
        return None

    def decrease_resolutions(self, param):
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


    def rotate_images(self, angle=20, r=1) -> None:
        for folder_name in self.folders:
            images = self.folders[folder_name]
            images_rotated = []

            for image in images:
                for i in range(r):
                    images_rotated.append(rotate_image(image, angle * i))

            images.extend(images_rotated)

        self.print_status()
        return None


def save_img(image, directory, filename) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)

    full_path = os.path.join(directory, filename)

    cv2.imwrite(full_path, image)



def make_new_dir(new_dir) -> None:
    current_dir = os.getcwd()
    file_list = os.listdir()
    if new_dir not in file_list:
        os.mkdir(new_dir)
    os.chdir(current_dir)
    return None


def main():
    processor = ImageProcessor()
    processor.load_images("data")
    processor.rotate_images(angle=20, r=1)
    processor.decrease_resolutions(3) # 168x168 * (1/3) = 56x56
    processor.reduce_colors(color_amount=2)
    processor.replace_darkest_color(new_color=(0,0,0)) # zamienia tlo na czarne
    processor.mirror()
    processor.save("data")


if __name__ == '__main__':
    main()