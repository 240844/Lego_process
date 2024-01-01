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


def main():
    processor = ImageProcessor()
    processor.load_images("data")
    processor.rotate_images(20, 1)
    processor.decrease_resolutions(3) # 168x168 * (1/3) = 56x56
    processor.reduce_colors(color_amount=2)
    processor.replace_darkest_color(new_color=(0, 0, 0)) # zamienia tlo na czarne
    #processor.mirror()
    processor.save("data")


if __name__ == '__main__':
    main()
