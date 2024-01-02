from help_func import *


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
    new_image = np.zeros((image.shape[0], image.shape[1], 3))
    img_avg = get_avg(image)
    for x in range(image.shape[0]):
        for y in range(image.shape[1]):
            new_image[x, y] = np.asarray(img_avg)
    x_offset = int(image.shape[0] / 4)
    y_offset = int(image.shape[1] / 4)
    width = int(image.shape[1] * scale / 100)
    height = int(image.shape[0] * scale / 100)
    dim = (width, height)
    img = cv2.resize(image, dim)
    new_image[y_offset:y_offset + img.shape[0], x_offset:x_offset + img.shape[1]] = img
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

    def replace_darkest_color(self, new_color: tuple[int, int, int] = (0, 0, 0)) -> None:
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

    def reduce_colors(self, color_amount: int = 2) -> None:
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

    def decrease_resolutions(self, param: int) -> None:
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

    def rotate_images(self, angle: int = 20, r: int = 1) -> None:
        for folder_name in self.folders:
            images = self.folders[folder_name]
            images_rotated = []

            for image in images:
                for i in range(r):
                    images_rotated.append(rotate_image(image, angle*i))

            images.extend(images_rotated)

        self.print_status()
        return None

    def zoom_all(self) -> None:
        for folder_name in self.folders:
            images = self.folders[folder_name]
            images_zoomed = []
            for image in images:
                images_zoomed.append(zoom_out(image, scale=60))
                images_zoomed.append(zoom_out(image))
                images_zoomed.append(zoom_in(image))
            images.extend(images_zoomed)
        self.print_status()
        return None


def main():
    processor = ImageProcessor()
    processor.load_images("data")
    #processor.rotate_images(20, 1)
    processor.zoom_all()
    processor.decrease_resolutions(3)  # 168x168 * (1/3) = 56x56
    processor.reduce_colors(color_amount=2)
    processor.replace_darkest_color(new_color=(0, 0, 0))  # zamienia tlo na czarne
    #processor.mirror()
    processor.save("data")


if __name__ == '__main__':
    main()
