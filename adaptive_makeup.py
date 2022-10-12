# author: Pu Muxin, date: 2021/8/14

from cv2 import imread, cvtColor, COLOR_RGB2BGR
from facial_landmarks_detection.skin_detector import detector
from makeup_features.eyeliner import eyeliner
from level_makeup.level_lipstick import lipstick
from makeup_features.blushes import blushes
from makeup_features.eyeshadow import eyeshadow
from shutil import copy
import matplotlib.pyplot as plt
import numpy as np
import os


def single_makeup(image_path, mask_path):
    skin_intensity, _ = detector(image_path, mask_path)
    img = blushes(imread(image_path), intensity=1-skin_intensity)
    img = eyeshadow(cvtColor(img, COLOR_RGB2BGR), intensity=1-skin_intensity)
    img = eyeliner(cvtColor(img, COLOR_RGB2BGR))
    img = lipstick(cvtColor(img, COLOR_RGB2BGR), 'moderate')
    return img


def group_makeup(src_dir, mask_path, dst_dir, folder_dir, outlier_dir):
    files_dir = src_dir+folder_dir
    for file_name in os.listdir(files_dir):
        file_path = files_dir + '/' + file_name
        try:
            this_makeup = single_makeup(file_path, mask_path)
            plt.imsave(dst_dir + folder_dir + '/' + file_name, this_makeup.astype(np.uint8))
        except Exception:
            copy(file_path, dst_dir+outlier_dir)


def place_makeup(src_dir, dst_dir, mask_path, element):
    for i in range(len(element[0])):
        for j in range(len(element[1])):
            for z in range(len(element[2])):
                folder_dir = '/' + element[0][i] + '/' + element[1][j] + '/' + element[2][z]
                outlier_dir = '/' + element[0][i] + '/' + element[1][j] + '/' + 'outlier'
                group_makeup(src_dir, mask_path, dst_dir, folder_dir, outlier_dir)


def adaptive_makeup(src_dir, dst_dir, mask_path):
    for file_name in os.listdir(src_dir):
        file_path = src_dir + '/' + file_name
        folder_dst_dir = dst_dir + '/adaptive'
        file_dst_dir = folder_dst_dir + '/real/' + file_name
        outlier_dir = folder_dst_dir + '/outlier/' + file_name
        try:
            this_makeup = single_makeup(file_path, mask_path)
            plt.imsave(file_dst_dir, this_makeup.astype(np.uint8))
        except Exception:
            copy(file_path, outlier_dir)
