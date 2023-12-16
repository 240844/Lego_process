import cv2
import numpy as np
import os

from dataClass import image_processing


# Funkcja do zmniejszenia rozdzielczości obrazu
def decrease_resolution(img, step=2):
    return None


# Funkcja do def mirror_img(img):
#     img = cv2.flip(img, 1)
#     return imgobrócenia obrazu lustrzanie


def rotate_img(img, background="avg"):
    return img


# Funkcja do zapisu obrazu o nazwie name i w folderze directory
# pamiętaj by dodać format pliku bo inaczej się zepsuje
def save_img(img, name: str, directory: str) -> None:
    cdir = os.getcwd()
    os.chdir(directory)
    cv2.imwrite(name, img)
    os.chdir(cdir)
    return None


def rename_files_in_dir(directory: str = "img_dir") -> None:
    temp_ = directory[directory.rfind('/')+1:]
    for count, filename in enumerate(os.listdir(directory)):
        format_ = filename[filename.rfind('.'):]
        new_name = f'{temp_}_img_{count}{format_}'
        print(f'{directory}: {filename} | {new_name}')
        src = f'{directory}/{filename}'
        dst = f'{directory}/{new_name}'
        os.rename(src, dst)
    return None


def make_new_dir(new_dir: str, dst_dir: str) -> None:
    current_dir = os.getcwd()
    os.chdir(dst_dir)
    file_list = os.listdir()
    if new_dir not in file_list:
        os.mkdir(new_dir)
    os.chdir(current_dir)
    return None


def create_mirror_img(dir_name: str, dst_name: str) -> None:
    for count, filename in enumerate(os.listdir(dir_name)):
        name = f'{dir_name}/{filename}'
        img = cv2.imread(name)
        ind_start = filename.rfind('/')
        ind_end = filename.rfind('.')
        new_dir_name = f'{filename[ind_start+1:ind_end]}_mirror'
        make_new_dir(new_dir_name, dst_name)
        #img = mirror_img(img)
        new_dir_name = f'{dst_name}/{new_dir_name}'
        save_img(img, f'Test_{count}.jpg', new_dir_name)
    return None


def process(rename_files: bool = True) -> None:
    dir_name = "img_dir"
    current_dir = os.getcwd()
    make_new_dir("Test", current_dir)
    test_dir = f'{current_dir}/Test'
    for count, dirname in enumerate(os.listdir(dir_name)):
        temp_ = f'{dir_name}/{dirname}'
        if rename_files:
            rename_files_in_dir(temp_)
        create_mirror_img(temp_, test_dir)

    return None


if __name__ == "__main__":
    processing = image_processing()
    processing.__int__("img_dir")
    processing.mirror()  # 2x
    #processing.rotate()  # 4x
    processing.save("img_dir_processed")
