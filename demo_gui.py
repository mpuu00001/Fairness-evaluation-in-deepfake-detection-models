"""
author: Nyee Thoang Lim

default: run on sample_images dataset file hierarchy

sample_images dataset file hierarchy
-   male
    - test
        - real (3 images)
        - fake (3 images)
-female
    - test
        - real (3 images)
        - fake (3 images)
"""

from level_makeup import *


def user_interface(this_src_dir, this_dst_dit = None):
    """
    a simple user interface which applys makeup based on user inputs
    user input - full/partial makeup, light/medium/heavy makeup, eye/blush/lip makeup, separate/combined output saving option

    Args:
        this_src_dir: source path to input image dataset
        this_dst_dit: destination path to save output
    """

    # path to image mask to find intensity
    this_mask_path = 'mask.jpg'

    # folder directories (gender - male/female) (deepfake - real/fake)
    # element = [['female', 'male'], ['test'], ['fake', 'real']]
    # element = [['Female', 'Male']]
    element = [['Female']]

    # verify user inputs
    choices = ['1', '2']
    regions = ['eye', 'lip', 'blush']
    levels = ['light', 'medium', 'heavy']

    # store the makeup features from user input
    features = []

    # get makeup choice
    while True:
        choice = input("Enter your choice (1: full makeup; 2: partial makeup): \n")
        if choice not in choices:
            print("Invalid choice input! Please try again!")
        else:
            break

    # get makeup level
    while True:
        level = input("Enter the makeup level (light/ medium/ heavy): \n")
        if level not in levels:
            print("Invalid level input! Please try again!")
        else:
            break

    # apply full/ partial makeup
    if choice == '1': # complete makeup
        place_makeup(this_src_dir, this_dst_dir, this_mask_path, element, level, None, None)
    else: # partial makeup
        while True: # makeup component
            feature = input("Enter the makeup component required (eye/ lip/ blush)(Enter 1 to exit user input): \n")
            if feature == '1': # end user input for makeup feature selection
                break
            else:
                if feature in features: # no repeated makeup component allowed
                    print("Option repeated! Please try again!")
                elif feature in regions:
                    features.append(feature)
                else:
                    print("Invalid input! Please try again!")

        while True: # output saving option
            selection = input("Enter option (1: separate makeup, 2: combined makeup): \n")
            if selection not in choice:
                print("Invalid save option input! Please try again! ")
            else:
                break

        if selection == '1': # separate: each feature has its own folder
            for feature in features:
                place_makeup(this_src_dir, this_dst_dir, this_mask_path, element, level, feature, None)
        else: # combine: combine the features into a single folder
            place_makeup(this_src_dir, this_dst_dir, this_mask_path, element, level, None, features)

    print("Execution successful!")

if __name__ == "__main__":

    # path to image dataset
    this_src_dir = "/Users/muxin/PyCharm/makeup_application/sample_images"
    # this_src_dir = "../DeepFace-gender-bias-detection/data/LFW_gender"

    # path to output destination folder
    # this_dst_dir = "../DeepFace-gender-bias-detection/data/LFW_gender_makeup_heavy"
    # this_dst_dir = "../DeepFace-gender-bias-detection/data/LFW_gender_makeup_light"
    # this_dst_dir = "../DeepFace-gender-bias-detection/data/LFW_gender_makeup_medium"
    # this_dst_dir = "../DeepFace-gender-bias-detection/data/LFW_gender_"

    this_dst_dir = "/Users/muxin/PyCharm/makeup_application/output_images"

    user_interface(this_src_dir, this_dst_dir)





