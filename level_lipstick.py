"""
Apply lipstick according to different levels

author: Nyee Thoang Lim

reference:
https://github.com/hriddhidey/visage/blob/ac58ccd95c832b34ffec61318093e3901539f988/visage/apply_makeup.py#L239
"""
import imutils
from level_functions import *
import itertools

def lipstick(image, facial_landmark, level = 'light'):
    """
    Apply lipstick to a given image with specified level.

    Args:
        image: given face image
        level: makeup level
    """
    if image.size == 0:
        print("Image is empty!")
        return

    if level == 'light':
        Rg = 255.
        Gg = 162.
        Bg = 173.
    elif level == 'medium':
        Rg = 255.
        Gg = 142.
        Bg = 153.
    else:
        Rg = 225.
        Gg = 95.
        Bg = 95.

    lip_x = []
    lip_y = []

    # completes the boundary coordinates for lipline
    def fill_lip_lines(outer, inner):
        outer_curve = zip(outer[0], outer[1])
        inner_curve = zip(inner[0], inner[1])
        count = len(inner[0]) - 1
        last_inner = [inner[0][count], inner[1][count]]
        for o_point, i_point in itertools.zip_longest(
                outer_curve, inner_curve, fillvalue=last_inner
        ):
            line = interpolate.interp1d(
                [o_point[0], i_point[0]], [o_point[1], i_point[1]], 'linear')
            xpoints = list(np.arange(o_point[0], i_point[0], 1))
            lip_x.extend(xpoints)
            lip_y.extend([int(point) for point in line(xpoints)])

    # fill in color in lip region
    def fill_lip_solid(img, outer, inner):
        inner[0].reverse()
        inner[1].reverse()
        outer_curve = zip(outer[0], outer[1])
        inner_curve = zip(inner[0], inner[1])
        points = []
        for point in outer_curve:
            points.append(np.array(point, dtype=np.int32))
        for point in inner_curve:
            points.append(np.array(point, dtype=np.int32))
        points = np.array(points, dtype=np.int32)
        cv2.fillPoly(img, [points], (Rg, Gg, Bg))
        return img

    # helper function to separate coordinates into x,y coordinates accordingly
    def convert_xy(outer, inner):
        outer_curve = zip(outer[0], outer[1])
        inner_curve = zip(inner[0], inner[1])
        x_points = []
        y_points = []
        for point in outer_curve:
            x_points.append(point[0])
            y_points.append(point[1])
        for point in inner_curve:
            x_points.append(point[0])
            y_points.append(point[1])
        return x_points, y_points

    # actual implementation
    print("level lipstick")
    image, _, shape, height, width = compute_statistics(image, facial_landmark) # obtain facial landmarks and image dimensions

    # obtains coordinates of the lip region and interpolate a curve line around the lip region
    top_outer_lip_indices = [48, 49, 50, 51, 52, 53, 54]
    top_outer_lip = [shape[i] for i in top_outer_lip_indices]
    for i in range(1, len(top_outer_lip)-1, 1): # readjust the y coordinates to show contours
        top_outer_lip[i] = (top_outer_lip[i][0], top_outer_lip[i][1]+5)
    uol = draw_curve(top_outer_lip, 0)

    bottom_inner_lip_indices = [48, 60, 66, 67, 65, 64, 54]
    bottom_inner_lip = [shape[i] for i in bottom_inner_lip_indices]
    lil = draw_curve(bottom_inner_lip, 0)
    top_inner_lip_indices = [54, 64, 63, 62, 61, 60, 48]
    top_inner_lip = [shape[i] for i in top_inner_lip_indices]
    uil = draw_curve(top_inner_lip, 2)

    bottom_outer_lip_indices = [54, 55, 56, 57, 58, 59, 48]
    bottom_outer_lip = [shape[i] for i in bottom_outer_lip_indices]
    for i in range(1, len(bottom_outer_lip)-1, 1): # readjust the y coordinates to show contours
        bottom_outer_lip[i] = (bottom_outer_lip[i][0], bottom_outer_lip[i][1]-2)
    lol = draw_curve(bottom_outer_lip, 2)

    # obtain the complete lip boundary line and fill in lip color
    fill_lip_lines(uol, uil)
    fill_lip_lines(lol, lil)
    image_copy = image.copy()
    image_copy = fill_lip_solid(image_copy, uol, uil)
    image_copy = fill_lip_solid(image_copy, lol, lil)

    # smoothen the lip color
    upper_x_points, upper_y_points = convert_xy(uol, uil)
    lower_x_points, lower_y_points = convert_xy(uol, uil)
    image_copy = smoothen_lipstick(image_copy, image, height, width, upper_x_points, upper_y_points)
    image_copy = smoothen_lipstick(image_copy, image, height, width, lower_x_points, lower_y_points)
    image_copy = imutils.resize(image_copy, width=256) # resize to MesoNet input requirement
    return image_copy

