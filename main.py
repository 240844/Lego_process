import cv2
import os
import numpy as np


def decrease_resolution(img, step=10):
    img = img[::step, ::step]
    return img


def treshold(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    return thresh


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
                image = decrease_resolution(image, 6)
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

                print(dir + "\\" + filename)
                save_img(image, dir, filename)

        print("saved")
        return None

    def auto_treshold(self):

        folders_tresholded = {}

        for folder_name in self.folders:
            images = self.folders[folder_name]

            images_tresholded = []
            for image in images:
                images_tresholded.append(treshold(image))

            folders_tresholded.update({folder_name: images_tresholded})
            images.extend(images_tresholded)

        self.folders = folders_tresholded
        self.print_status()
        return None

    def rotate_image(self, image, angle):
        image_center = tuple(np.array(image.shape[1::-1]) / 2)
        rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
        result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
        img_avg = get_avg(result)
        for x in range(result.shape[0]):
            for y in range(result.shape[1]):
                if np.array_equal([0, 0, 0], result[x, y]):
                    result[x, y] = np.asarray(img_avg)
        return result

    def rotate_images(self, angle=20, r=1) -> None:
        for folder_name in self.folders:
            images = self.folders[folder_name]
            images_rotated = []

            for image in images:
                for i in range(r):
                    images_rotated.append(self.rotate_image(image, angle*i))

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


def get_avg(img):
    output1 = np.average(img[:, :, 0])
    output2 = np.average(img[:, :, 1])
    output3 = np.average(img[:, :, 2])
    output = [output1, output2, output3]
    return output


def fun(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv2.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv2.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv2.INTER_LINEAR)
    for x in range(result.shape[0]):
        for y in range(result.shape[1]):
            t = result[x, y]
            if np.array_equal([0, 0, 0], t):
                result[x, y] = np.asarray([255, 255, 255])
    return result


def main():

    t_img = cv2.imread("data/apple/32374789.png")
    print(type(t_img))
    d_img = fun(t_img, 20)
    get_avg(t_img)
    cv2.imwrite("test1.png", d_img)

    processor = image_processing()
    processor.load_images("data")
    processor.rotate_images()
    processor.mirror()
    processor.auto_treshold()

    processor.save("data")


if __name__ == '__main__':
    main()