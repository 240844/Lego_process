import cv2
import os


class image_processing:

    def __int__(self, path: str):
        self.folders = {}
        self.directory_path = path

        for folder_name in os.listdir(path):
            images = []
            folder_name_ = f'{path}/{folder_name}'
            for name in os.listdir(folder_name_):
                name = f'{folder_name_}/{name}'
                image = cv2.imread(name)
                image = decrease_resolution(image)
                images.append(image)
            self.folders.update({folder_name: images})

        self.print_status()

    def mirror(self) -> None:

        folders_mirrored = {}

        for folder_name in self.folders:
            images = self.folders[folder_name]

            images_flipped = []
            for image in images:
                images_flipped.append(cv2.flip(image, 1))

            folders_mirrored.update({folder_name: images_flipped})
            images.extend(images_flipped)

        self.print_status()
        return None

    def print_status(self) -> None:
        print("status:")
        for folder_name in self.folders:
            print(folder_name, "-", len(self.folders[folder_name]), "images")

        return None

    def save(self, path: str) -> None:
        cdir = os.getcwd()
        dir_name = f'{self.directory_path}_processed'
        make_new_dir(dir_name, cdir)
        for folder_name in self.folders:
            dst_dir = f'{cdir}/{self.directory_path}_processed/'
            dir_ = f'{self.directory_path}_processed/{folder_name}'
            make_new_dir(folder_name, dst_dir)
            for i, image in enumerate(self.folders[folder_name]):
                image_name = f'{folder_name}_{i}.jpg'
                save_img(image, image_name, dir_)
        return None


def save_img(img, name: str, directory: str) -> None:
    cdir = os.getcwd()
    os.chdir(directory)
    cv2.imwrite(name, img)
    os.chdir(cdir)
    return None


def decrease_resolution(img, step=8):
    img = img[::step, ::step]
    return img


def make_new_dir(new_dir: str, dst_dir: str) -> None:
    current_dir = os.getcwd()
    os.chdir(dst_dir)
    file_list = os.listdir()
    if new_dir not in file_list:
        os.mkdir(new_dir)
    os.chdir(current_dir)
    return None
