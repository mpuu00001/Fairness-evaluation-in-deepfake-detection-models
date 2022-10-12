""" Apply blushes

author: Nyee Thoang Lim
"""


import imutils
# from makeup_features.functions import *
from makeup_features.functions import compute_statistics, apply_color, smoothen, get_boundary_points, get_interior_points
# from functions import *


def blushes(image, intensity = 0.5, Rg=160., Gg=70., Bg=101.):
    """
    Apply lipstick to a given image with specified level.

    Args:
        image: given face image
        intensity: blush intensity
        Rg, Gg, Bg: RGB values
    """
    if intensity > 0.5:
        intensity = 0.5

    rgb = [Rg, Gg, Bg]
    for channel in rgb:
        if channel < 0 or channel > 255:
            print("Invalid RGB values!")
            Rg = 100
            Gg = 35
            Bg = 45

    # smoothen blushes onto the cheek region
    def apply_blushes(shape, indices, image_copy, image, height, width):
        cheek_x = [shape[i][0] for i in indices]
        cheek_y = [shape[i][1] for i in indices]
        cheek_x, cheek_y = get_boundary_points(cheek_x, cheek_y)
        cheek_y, cheek_x = get_interior_points(cheek_x, cheek_y)
        image_copy = smoothen(image_copy, image, height, width, cheek_x,cheek_y)
        return image_copy

    # actual implementation
    image, d, shape, height, width = compute_statistics(image) # obtain facial landmarks and image dimension
    image_copy = image.copy()
    image = apply_color(image, intensity, Rg, Gg, Bg, height, width)

    # apply blush on cheeks
    right_cheek_indices = [15, 14, 13, 35, 45]
    left_cheek_indices = [1, 2, 3, 48, 31, 36]
    image_copy = apply_blushes(shape, right_cheek_indices, image_copy, image, height, width)
    image_copy = apply_blushes(shape, left_cheek_indices, image_copy, image, height, width)

    image_copy = imutils.resize(image_copy, width=256) # resize to Mesonet input requirement

    return image_copy