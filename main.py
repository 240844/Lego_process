import cv2
import os

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
    processor.auto_treshold()
    processor.mirror()
    processor.save("data")


if __name__ == '__main__':
    main()