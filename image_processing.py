import numpy as np

from help_func import *


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

                dir_ = cdir + "\\" + self.directory_path + "_processed\\" + folder_name
                filename = folder_name + "_" + str(i) + ".png"

                #print(dir + "\\" + filename)
                save_img(image, dir_, filename)

        print("saved")
        return None

    def replace_darkest_color(self, new_color=(0, 0, 0)) -> None:
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

    def reduce_colors(self, color_amount=2) -> None:
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

    def decrease_resolutions(self, param) -> None:
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
                    images_rotated.append(rotate_image(image, angle*i))

            images.extend(images_rotated)

        self.print_status()
        return None

    def zoom_out(self, image):
        new_image = np.zeros((image.shape[0], image.shape[1], 3))
        img_avg = get_avg(image)
        for x in range(image.shape[0]):
            for y in range(image.shape[1]):
                new_image[x, y] = np.asarray(img_avg)
        x_offset = int(image.shape[0] / 4)
        y_offset = int(image.shape[1] / 4)
        img = decrease_resolution(image, step=2)
        new_image[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
        return new_image

    def zoom_in(self, image):
        x_offset = int(image.shape[0] / 4)
        y_offset = int(image.shape[1] / 4)
        n_width = int(image.shape[0] / 2)
        n_height = int(image.shape[1] / 2)
        new_image = np.zeros((n_width, n_height, 3))
        for x in range(n_width):
            for y in range(n_height):
                print(x)
                new_image[x, y] = image[x + x_offset, y + y_offset]
        return new_image

    def zoom_out_all(self) -> None:
        for folder_name in self.folders:
            images = self.folders[folder_name]
            images_zoomed = []

            for image in images:
                images_zoomed.append(self.zoom_out(image))

            images.extend(images_zoomed)

        self.print_status()
        return None

def main():
    processor = ImageProcessor()
    processor.load_images("data")
    processor.rotate_images(20, 1)
    processor.decrease_resolutions(3)  # 168x168 * (1/3) = 56x56
    processor.reduce_colors(color_amount=2)
    processor.replace_darkest_color(new_color=(0, 0, 0))  # zamienia tlo na czarne
    #processor.mirror()
    processor.save("data")


if __name__ == '__main__':
    main()
