"""
author: Muxin Pu
modified on level_makeup.level_makeup.py by Nyee Thoang Lim
add-on: allow partial makeup combinations
"""

from cv2 import imread, cvtColor, COLOR_RGB2BGR
from skin_detector import detector
from eyeliner import eyeliner
from level_lipstick import lipstick
from level_blushes import blushes
from level_eyeshadow import eyeshadow
import matplotlib.pyplot as plt
import numpy as np
import os
from facial_landmark import detect_facial_landmark


# apply full set makeup with specified level to an image
def single_makeup(image_path, mask_path, this_level):
    """
    Apply full makeup with specified level to an image

    Args:
         image_path: path to image
         mask_path: path to mask image
         this_level: makeup level
    """
    skin_intensity, _ = detector(image_path, mask_path)  # obtain skin intensity value
    facial_landmark = detect_facial_landmark(imread(image_path))

    # print("Start drawing blushes")
    img = blushes(imread(image_path), facial_landmark, intensity=1 - skin_intensity, level=this_level)
    # print("Blushes are done")

    # print("Start drawing eyeshadows")
    img = eyeshadow(cvtColor(img, COLOR_RGB2BGR), facial_landmark, intensity=1 - skin_intensity, level=this_level)
    # print("Eyeshadows are done")

    # print("Start drawing eyeliner")
    img = eyeliner(cvtColor(img, COLOR_RGB2BGR), facial_landmark)
    # print("eyeliner are done")

    # print("Start drawing Lipsticks")
    img = lipstick(cvtColor(img, COLOR_RGB2BGR), facial_landmark, this_level)
    # print("Lipsticks are done")

    plt.imshow(img)
    plt.show()
    return img


def combine_makeup(image_path, mask_path, this_level, combined_regions):
    """
    Apply makeup based on a given combination of makeup regions with specified level to an image

    Args:
        image_path: path to image
        mask_path: path to mask
        this_level: makeup level
        combine_regions: list of makeup regions intended
    """
    skin_intensity, _ = detector(image_path, mask_path)
    img = imread(image_path)
    for opt_feature in combined_regions:
        if opt_feature != combined_regions[0]:
            img = cvtColor(img, COLOR_RGB2BGR)
        if opt_feature == 'eye':
            img = eyeshadow(img, intensity=1 - skin_intensity, level=this_level)
            img = eyeliner(cvtColor(img, COLOR_RGB2BGR))
        elif opt_feature == 'blush':
            img = blushes(img, intensity=1 - skin_intensity, level=this_level)
        elif opt_feature == 'lip':
            img = lipstick(img, this_level)

    return img


def feature_makeup(image_path, mask_path, this_level, opt_regions):
    """
    Apply makeup based on a certain region with specified level to an image

    Args:
        image_path: path to image
        mask_path: path to mask
        this_level: makeup level
        opt_regions: makeup region intended
    """
    skin_intensity, _ = detector(image_path, mask_path)
    img = imread(image_path)
    if opt_regions == 'eye':
        img = eyeshadow(img, intensity=1 - skin_intensity, level=this_level)
        img = eyeliner(cvtColor(img, COLOR_RGB2BGR))
    elif opt_regions == 'blush':
        img = blushes(img, intensity=1 - skin_intensity, level=this_level)
    elif opt_regions == 'lip':
        img = lipstick(img, this_level)

    return img


def group_makeup(src_dir, mask_path, dst_dir, element, this_level, opt_regions=None, combined_regions=None):
    """
    Apply makeup with specified level and selection to all images within a source path and save to a destination path

    Args:
        src_path: path to image dataset
        mask_path: path to mask
        dst_dir: destination directory
        element: folder name
        this_level: makeup level
        opt_regions: makeup region intended
        combined_regions: list of makeup regions intended
    """
    files_dir = src_dir + "/" + element  # construct image path
    for file_name in os.listdir(files_dir):
        file_path = files_dir + '/' + file_name  # get image file
        print("Processing " + file_path + "...")
        if opt_regions is not None:
            folder_dest_dir = dst_dir + '/' + opt_regions + element
        else:
            folder_dest_dir = dst_dir + '/' + element
        # folder_dest_dir = folder_dest_dir + "(" + this_level + ")"
        folder_dest_dir = folder_dest_dir

        if not os.path.exists(folder_dest_dir):
            print("Destination path is absent and is therefore created! ")
            os.makedirs(folder_dest_dir)

        file_dst_dir = folder_dest_dir + '/' + file_name

        try:
            if opt_regions is None and combined_regions is None:  # full makeup
                this_makeup = single_makeup(file_path, mask_path, this_level)
            elif combined_regions is not None:  # combined partial makeup, save to a single output path
                this_makeup = combine_makeup(file_path, mask_path, this_level, combined_regions)
            else:  # partial makeup, save to individual output folders
                this_makeup = feature_makeup(file_path, mask_path, this_level, opt_regions)
            plt.imsave(file_dst_dir, this_makeup.astype(np.uint8))
            # print(file_path + " success to be executed!")
        except Exception as e:
            print(e)
            # with open("/Users/muxin/PyCharm/makeup_application/error_report.txt", "a") as f:
            #     f.write(file_path + " fails to be executed!\n")
            print(file_path + " fails to be executed!---------------------")
            pass

def place_makeup(src_dir, dst_dir, mask_path, element, this_level, opt_regions=None, combined_regions=None):
    """
    Go through every directory of the specified source path to apply makeup onto each image folder within the source directory

    Args:
        src_dir: path to image dataset directory
        dst_dir: destination directory
        mask_path: path to mask
        element: nested list of directory's in-depth folders
        this_level: makeup level
        opt_regions: makeup region intended
        combined_regions: list of makeup regions intended
    """
    for i in range(len(element[0])):  # gender folder
        data_gender = os.listdir(src_dir + '/' + element[0][i])
        for people in data_gender:
            if people != ".DS_Store":
                people_dir = f"{element[0][i]}/{people}"
                print("people_dir: " + people_dir)
                try:
                    group_makeup(src_dir, mask_path, dst_dir, people_dir, this_level, opt_regions,
                                 combined_regions)
                except FileNotFoundError:
                    print("Image source path: " + people_dir + " is absent! No images available, "
                                                               "please check the path again!")


mask_path = '/Users/muxin/PyCharm/makeup_application/mask.jpg'
this_src_dir = "/Users/muxin/PyCharm/makeup_application/sample_images"
this_dst_dir = "/Users/muxin/PyCharm/makeup_application/output_images"
element = [['Female', 'Male']]
this_level = 'light'
# with open('/Users/muxin/PyCharm/makeup_application/error_report.txt', 'w') as f:
#     f.write('')
# place_makeup(this_src_dir, this_dst_dir, mask_path, element, this_level, opt_regions=None, combined_regions=None)


# image_path = "/Users/muxin/PyCharm/makeup_application/output_images/Female/test/Justine_Pasek_0005.jpg"
# img = single_makeup(image_path, mask_path, this_level)

# image_path = "/Users/muxin/PyCharm/makeup_application/sample_images/Female/test/Roseanne_Barr_0001.jpg"
# img = single_makeup(image_path, mask_path, this_level)
#
image_path = "/Users/muxin/PyCharm/makeup_application/sample_images/Male/test/Mike_Weir_0003.jpg"
img = single_makeup(image_path, mask_path, this_level)
