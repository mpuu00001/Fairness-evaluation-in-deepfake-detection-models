# author: Pu Muxin, date: 2021/8/4

from facial_landmark import *
from cv2 import imread, rectangle
from imutils import resize
import numpy as np


def average(i, int_lst):
    return sum(x[i] for x in int_lst) // len(int_lst)


def select_marks(shape, marks, k):
    for i in range(2):
        marks[i] = list(shape[marks[i]])
        marks[i][0] = marks[i][0] + k if i == 0 else marks[i][0] - k
        marks.append([marks[i][0], marks[i][1] + k])


def detect_skin_color(file_path, marks, k, mask_path):
    facial_landmark = detect_facial_landmark(imread(file_path))
    print()
    image = facial_landmark[0]
    shape = facial_landmark[1]
    mask = resize(imread(mask_path), width=500)

    select_marks(shape, marks, k)
    rectangle(mask, marks[0], marks[1], (0, 0, 0), k+5)
    skin = [[image[x, y][0], image[x, y][1], image[x, y][2]] for [x, y] in marks]
    [r, g, b] = [average(0, skin), average(1, skin), average(2, skin)]

    return image, mask, [r, g, b]


def detect_skin_intensity(image, mask):
    lock = np.where(mask == 0)
    pixels = image[lock]
    skin_intensity = np.mean(pixels)/255
    return skin_intensity


def detector(file_path, mask_path):
    image, mask, [r, g, b] = detect_skin_color(file_path, [21, 22], 20, mask_path)
    skin_intensity = detect_skin_intensity(image, mask)
    return skin_intensity, [r, g, b]


# Example
# file = '/home/nyeethoang/Documents/New_makeup/test_images/056_0009.jpg'
# mask = '/home/nyeethoang/Documents/New_makeup/mask.jpg'
# intensity, [R, G, B] = detector(file, mask)
# print(intensity)
# print(R, G, B)

