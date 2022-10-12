"""
Apply eyeshadow to different levels

author: Nyee Thoang Lim
modified by: Muxin date: 2022/9/21
"""
import imutils
from level_functions import *


def eyeshadow(image, facial_landmark, intensity=0.5, level='light'):
    """
    Apply eyeshadow to a given image with specified level.

    Args:
        image: given face image
        intensity: eyeshadow intensity
        level: makeup level
    """

    if image.size == 0:
        print("Image is empty!")
        return

    if intensity > 1 or intensity < 0:
        print("Invalid intensity value")
        intensity = 0.5

    if intensity > 0.75:
        print('bright')
        origin = 'bright'  # bright image
        if level == 'light':
            intensity = 0.45
            Rg = 100.
            Gg = 10.
            Bg = 10.
        elif level == 'medium':
            intensity = 0.7
            Rg = 150.
            Gg = 15.
            Bg = 30.
        else:
            intensity = 0.85
            Rg = 175.
            Gg = 50.
            Bg = 60.
    elif 0.35 < intensity <= 0.75:  # moderate brightness image
        origin = 'moderate'

        if level == 'light':
            intensity = 0.6
            Rg = 155.
            Gg = 15.
            Bg = 30.
        elif level == 'medium':
            intensity = 0.8
            Rg = 180.
            Gg = 30.
            Bg = 50.
        else:
            intensity = 0.9
            Rg = 215.
            Gg = 45.
            Bg = 80.
    else:  # dark image
        origin = 'dark'
        if level == 'light':
            intensity = 0.75
            Rg = 200.
            Gg = 130.
            Bg = 125.
        elif level == 'medium':
            intensity = 0.80
            Rg = 235.
            Gg = 135.
            Bg = 135.
        else:
            intensity = 0.85
            Rg = 250.
            Gg = 138.
            Bg = 140.

    # helper function to get eyeshadow region coordinates above upper eyelid
    def find_point(shape, coor, facial_point=None, x=None):
        if facial_point:
            x = shape[facial_point][0]
            y = shape[facial_point][1]
        else:
            y = min(shape[19][1], shape[20][1]) - 1

        temp1 = [item[1] for item in coor if item[0] == x]
        temp2 = []
        # print("\t\tcoor: " + str(coor))
        # print("\t\tx: " + str(x))
        # print("\t\ty: " + str(y))

        for item in coor:
            if item[0] == x:
                temp2 = [item[1]]
        if not temp2:
            index = 0 if x == min(coor[0][0], x) else len(coor)//2
            x, temp2 = coor[index][0], [coor[index][1]]
        # print("\t\ttemp1: " + str(temp1))
        # print("\t\ttemp2: " + str(temp2))
        # print('\tMay have Error in line 107!!!')
        eyeline_y = temp2[0]
        eyeshadow_height = (eyeline_y - y) * 3 // 7
        top_point = (x, eyeline_y - eyeshadow_height)
        return top_point

    # apply eyeshadow onto the region
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
        # print("\t1: ")
        eyeshadow_tip1 = find_point(shape, zip_coor, index1)
        # print("\t1 done")

        # print("\t2: ")
        eyeshadow_tip3 = find_point(shape, zip_coor, index2)
        # print("\t2 done")

        eyeshadow_tip3 = (eyeshadow_tip3[0], eyeshadow_tip3[1] - 3)
        mid_tip_x = (eyeshadow_tip1[0] + eyeshadow_tip3[0]) // 2

        # print("\t3: ")
        eyeshadow_tip2 = find_point(shape, zip_coor, None, mid_tip_x)
        # print("\t3 done")

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
        image_copy = smoothen_eyeshadow(image_copy, image, height, width, eyeshadow_lower_x, eyeshadow_lower_y, origin,
                                        level)
        return image_copy

    # actual implementation
    print("level eyeshadow")
    image, _, shape, height, width = compute_statistics(image, facial_landmark) # obtain facial landmarks, image dimension
    print()
    image_copy = image.copy()
    image = apply_color(image, intensity, Rg, Bg, Gg, height, width)

    # obtain eye landmarks and apply eyeshadow
    left_eyeshadow_indices = [36, 37, 38, 39, 38, 37, 36]
    right_eyeshadow_indices = [45, 44, 43, 42, 43, 44, 45]
    # image_copy = apply_eyeshadow(shape, left_eyeshadow_indices, image_copy, image, height, width, 19, 20)
    image_copy = apply_eyeshadow(shape, right_eyeshadow_indices, image_copy, image, height, width, 24, 23)
    image_copy = imutils.resize(image_copy, width=256) # resize to Mesonet input requirement
    return image_copy