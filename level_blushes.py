"""
Apply blushes according to different levels

author: Nyee Thoang Lim
"""
import imutils
from level_functions import *


def blushes(image, facial_landmark, intensity=0.5, level='light', ):
    """
    Apply lipstick to a given image with specified level.

    Args:
        image: given face image
        intensity: blush intensity
        level: makeup level
    """
    if image.size == 0:
        print("Image is empty!")
        return

    if intensity > 1 or intensity < 0:
        print("Invalid intensity value")
        intensity = 0.5

    if intensity > 0.75:
        origin = 'bright'  # bright image
        if level == 'light':
            intensity = 0.3
            Rg = 255.
            Gg = 195.
            Bg = 202.
        elif level == 'medium':
            intensity = 0.5
            Rg = 230.
            Gg = 143.
            Bg = 160.
        else:
            intensity = 0.65
            Rg = 220.
            Gg = 110.
            Bg = 140.
    elif 0.35 < intensity <= 0.75:  # moderate brightness image
        origin = 'moderate'
        if level == 'light':
            intensity = 0.35
            Rg = 125.
            Gg = 55.
            Bg = 60.
        elif level == 'medium':
            intensity = 0.5
            Rg = 135.
            Gg = 50.
            Bg = 60.
        else:
            intensity = 0.75
            Rg = 155.
            Gg = 45.
            Bg = 65.
    else:  # dark image
        origin = 'dark'
        if level == 'light':
            intensity = 0.4
            Rg = 220.
            Gg = 115.
            Bg = 125.
        elif level == 'medium':
            intensity = 0.65
            Rg = 210.
            Gg = 95.
            Bg = 100.
        else:
            intensity = 0.9
            Rg = 190.
            Gg = 85.
            Bg = 90.

    # smoothen blushes onto the cheek region
    def apply_blushes(shape, indices, image_copy, image, height, width):
        cheek_x = [shape[i][0] for i in indices]
        cheek_y = [shape[i][1] for i in indices]
        cheek_x, cheek_y = get_boundary_points(cheek_x, cheek_y)
        cheek_y, cheek_x = get_interior_points(cheek_x, cheek_y)
        image_copy = smoothen(image_copy, image, height, width, cheek_x, cheek_y, origin, level)
        return image_copy

    # actual implementation
    print("level blushes")
    image, d, shape, height, width = compute_statistics(image, facial_landmark) # obtain facial landmarks, image dimension
    print()
    image_copy = image.copy()
    image = apply_color(image, intensity, Rg, Gg, Bg, height, width)

    # apply blush on cheeks
    right_cheek_indices = [15, 14, 13, 35, 45]
    left_cheek_indices = [1, 2, 3, 48, 31, 36]
    image_copy = apply_blushes(shape, right_cheek_indices, image_copy, image, height, width)
    image_copy = apply_blushes(shape, left_cheek_indices, image_copy, image, height, width)
    image_copy = imutils.resize(image_copy, width=256) # resize to MesoNet input requirement
    return image_copy

