""" Apply eyeshadow

author: Nyee Thoang Lim
"""
import imutils

from makeup_features.functions import *


def eyeshadow(image, intensity=0.5, Rg=155., Gg=20., Bg=40.):
    """
    Apply eyeshadow to a given image .

    Args:
        image: given face image
        intensity: eyeshadow intensity
        Rg, Gg, Bg: RGB values
    """
    if intensity > 0.5: # avoid too bright exposure
        intensity = 0.5

    rgb = [Rg, Gg, Bg]
    for channel in rgb:
        if channel < 0 or channel > 255:
            print("Invalid RGB values!")
            Rg = 100
            Gg = 35
            Bg = 45

    # helper function to find points of eyeshadow region
    def find_point(shape, coor, facial_point=None, x=None):
        if facial_point:
            x = shape[facial_point][0]
            y = shape[facial_point][1]
        else:
            y = min(shape[19][1], shape[20][1]) - 1
        eyeline_y = [item[1] for item in coor
                     if item[0] == x][0]

        eyeshadow_height = (eyeline_y - y) * 3 // 7
        top_point = (x, eyeline_y - eyeshadow_height)
        return top_point

    # apply eyeshadow
    def apply_eyeshadow(shape, indices, image_copy, image, height, width, index1, index2):
        eyeshadow_lower_x = [shape[i][0] for i in indices]
        eyeshadow_lower_y = [shape[i][1] for i in indices]
        eyeshadow_lower_x, eyeshadow_lower_y = get_boundary_points(eyeshadow_lower_x,
                                                                   eyeshadow_lower_y)
        zip_coor = list(zip(eyeshadow_lower_x, eyeshadow_lower_y))

        # remove extra coordinates, ensure the eyelid points is a one-point width line
        zip_coor.sort()
        ind = 1
        curr_x = zip_coor[0][0]
        while ind < len(zip_coor):
            if zip_coor[ind][0] == curr_x:
                del zip_coor[ind]
            else:
                curr_x = zip_coor[ind][0]
                ind += 1

        # draw the eyeshadow upper curve
        eyeshadow_tip1 = find_point(shape, zip_coor, index1)
        eyeshadow_tip3 = find_point(shape, zip_coor, index2)
        eyeshadow_tip3 = (eyeshadow_tip3[0], eyeshadow_tip3[1] - 3)
        mid_tip_x = (eyeshadow_tip1[0] + eyeshadow_tip3[0]) // 2
        eyeshadow_tip2 = find_point(shape, zip_coor, None, mid_tip_x)
        eyeshadow_top_points = [zip_coor[0], eyeshadow_tip3, eyeshadow_tip2, eyeshadow_tip1, zip_coor[-1]]
        eyeshadow_upper_x, eyeshadow_upper_y = draw_curve(eyeshadow_top_points, 0)

        # draw whole boundary line for eyeshadow
        eyeshadow_lower_x, eyeshadow_lower_y = zip(*zip_coor)
        eyeshadow_lower_x = list(eyeshadow_lower_x)
        eyeshadow_lower_y = list(eyeshadow_lower_y)
        eyeshadow_lower_x = eyeshadow_upper_x + eyeshadow_lower_x
        eyeshadow_lower_y = eyeshadow_upper_y + eyeshadow_lower_y
        eyeshadow_lower_x = np.array(eyeshadow_lower_x)
        eyeshadow_lower_y = np.array(eyeshadow_lower_y)

        # get inner eyeshadow points
        eyeshadow_lower_y, eyeshadow_lower_x = get_interior_points(eyeshadow_lower_x,
                                                                   eyeshadow_lower_y)

        # smoothen the eyeshadow
        image_copy = smoothen(image_copy, image, height, width, eyeshadow_lower_x, eyeshadow_lower_y)

        return image_copy

    # actual implementation
    image, _, shape, height, width = compute_statistics(image) # obtain facial landmarks and image dimensions
    image_copy = image.copy()
    image = apply_color(image, intensity, Rg, Bg, Gg, height, width)

    # obtain upper eyelid coordinates, plot eyeshadow region and apply eyeshadow
    left_eyeshadow_indices = [36, 37, 38, 39, 38, 37, 36]
    right_eyeshadow_indices = [45, 44, 43, 42, 43, 44, 45]
    image_copy = apply_eyeshadow(shape, left_eyeshadow_indices, image_copy, image, height, width, 19, 20)
    image_copy = apply_eyeshadow(shape, right_eyeshadow_indices, image_copy, image, height, width, 24, 23)
    image_copy = imutils.resize(image_copy, width=256) # resize to MesoNet input requirement

    return image_copy
