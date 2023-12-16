import cv2
import os

import numpy as np


def decrease_resolution(img, step=10):
    img = img[::step, ::step]
    return img

def treshold(gray_image):
    ret, thresh = cv2.threshold(gray_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh


def rgb_to_grayscale(image):
    b, g, r = cv2.split(image)

    grayscale_image = 0.299 * r + 0.587 * g + 0.114 * b

    grayscale_image = np.uint8(grayscale_image)

    return grayscale_image


def reduce(image, num_colors=2):
    pixels = image.reshape((-1, 3))

    # Convert to float type
    pixels = np.float32(pixels)

    # Define criteria for k-means
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.2)

    # Apply k-means clustering
    _, labels, centers = cv2.kmeans(pixels, num_colors, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    # Convert back to 8-bit values
    centers = np.uint8(centers)

    # Map the labels to the centers
    segmented_image = centers[labels.flatten()]

    # Reshape back to the original image shape
    segmented_image = segmented_image.reshape(image.shape)
    return segmented_image


def get_darkest_color(image):
    gray_img = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Find the coordinates of the darkest pixel
    min_intensity_coord = np.unravel_index(np.argmin(gray_img), gray_img.shape)

    # Get the color of the darkest pixel in BGR format
    darkest_color = image[min_intensity_coord]
    return darkest_color
    pass


def replace_color(image, old_background_color, new_background_color):

    new_image = image.copy()
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            if np.all(image[x, y] == old_background_color):
                new_image[x, y] = new_background_color

    return new_image
    pass


class image_processing:


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
                image = decrease_resolution(image, 3)
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

        self.print_status()
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

    def auto_treshold(self):

        folders_tresholded = {}

        for folder_name in self.folders:
            images = self.folders[folder_name]

            images_tresholded = []
            for image in images:

                gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                tresholded = treshold(gray_image)
                images_tresholded.append(tresholded)

            folders_tresholded.update({folder_name: images_tresholded})
            images.extend(images_tresholded)

        self.folders = folders_tresholded
        self.print_status()
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
        self.print_status()
        return None

    def reduce_colors(self, colors=2):
        folders_edited = {}

        for folder_name in self.folders:
            images = self.folders[folder_name]

            images_edited = []
            for image in images:
                images_edited.append(reduce(image, colors))

            folders_edited.update({folder_name: images_edited})
            images.extend(images_edited)

        self.folders = folders_edited
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
    processor = image_processing()
    processor.load_images("data")
    processor.reduce_colors(2)
    processor.replace_darkest_color(new_color=(0,0,0))
    #processor.rotate() #TODO
    processor.save("data")


if __name__ == '__main__':
    main()