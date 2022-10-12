"""
Apply eyeliner

author: Nyee Thoang Lim

reference:
https://github.com/hriddhidey/visage/blob/ac58ccd95c832b34ffec61318093e3901539f988/visage/apply_makeup.py#L239
"""
import imutils

from functions import *


def eyeliner(image, facial_landmark, color=(42, 28, 28)):
    """
    Apply eyeliner to a given image.

    Args:
        image: given face image
        color: (R, G, B)
    """
    if image.size == 0:
        print("Image is empty!")
        return

    for channel in color:
        if channel < 0 or channel > 255:
            print("Invalid RGB values!")
            color = (42, 28, 28)

    # draw eyeliner on upper eyelid
    def draw_liner(img, x_points, y_points, kind, color):

        try:
            if not isinstance(x_points, list):
                raise TypeError
        except TypeError:
            print("x_points input shall be list")
            x_points = x_points.tolist()
            print(type(x_points))

        try:
            if not isinstance(y_points, list):
                raise TypeError
        except TypeError:
            print("y_points input shall be list")
            y_points = y_points.tolist()
            print(type(y_points))

        if len(x_points) != len(y_points):
            print("x_points length shall be equal to y_points length")
            return

        eye_x = []
        eye_y = []
        curve = interpolate.interp1d(x_points, y_points, 'quadratic')
        for point in np.arange(x_points[0], x_points[len(x_points) - 1] + 1, 1):
            eye_x.append(point)
            eye_y.append(int(curve(point)))
        if kind == 'left': # left eye
            y_points[0] -= 1
            y_points[1] -= 1
            y_points[2] -= 1
            x_points[0] -= 5
            x_points[1] -= 1
            x_points[2] -= 1
            curve = interpolate.interp1d(x_points, y_points, 'quadratic')
            count = 0
            for point in np.arange(x_points[len(x_points) - 1], x_points[0], -1):
                count += 1
                eye_x.append(point)
                if count < (len(x_points) / 2):
                    eye_y.append(int(curve(point)))
                elif count < (2 * len(x_points) / 3):
                    eye_y.append(int(curve(point)) - 1)
                elif count < (4 * len(x_points) / 5):
                    eye_y.append(int(curve(point)) - 2)
                else:
                    eye_y.append(int(curve(point)) - 3)
        elif kind == 'right': # right eye
            x_points[3] += 5
            x_points[2] += 1
            x_points[1] += 1
            y_points[3] -= 1
            y_points[2] -= 1
            y_points[1] -= 1
            curve = interpolate.interp1d(x_points, y_points, 'quadratic')
            count = 0
            for point in np.arange(x_points[len(x_points) - 1], x_points[0], -1):
                count += 1
                eye_x.append(point)
                if count < (len(x_points) / 2):
                    eye_y.append(int(curve(point)))
                elif count < (2 * len(x_points) / 3):
                    eye_y.append(int(curve(point)) - 1)
                elif count < (4 * len(x_points) / 5):
                    eye_y.append(int(curve(point)) - 2)
                elif count:
                    eye_y.append(int(curve(point)) - 3)
        curve = zip(eye_x, eye_y)
        points = []
        for point in curve:
            points.append(np.array(point, dtype=np.int32))
        points = np.array(points, dtype=np.int32)
        cv2.fillPoly(img, [points], color)
        return img

    # actual implementation
    image, _, shape, height, width = compute_statistics(image, facial_landmark) # obtain facial landmarks and image dimension

    # get coordinates of upper eyelid
    left_eyelid_indices = [36, 37, 38, 39]
    left_eyelid = [shape[i] for i in left_eyelid_indices]
    right_eyelid_indices = [42, 43, 44, 45]
    right_eyelid = [shape[i] for i in right_eyelid_indices]
    left_eyelid_x = [item[0] for item in left_eyelid]
    left_eyelid_y = [item[1] for item in left_eyelid]
    right_eyelid_x = [item[0] for item in right_eyelid]
    right_eyelid_y = [item[1] for item in right_eyelid]

    # draw eyeliner
    image = draw_liner(image, left_eyelid_x, left_eyelid_y, 'left', color)
    image = draw_liner(image, right_eyelid_x, right_eyelid_y, 'right', color)
    image = imutils.resize(image, width=256) # resize to MesoNet input requirement

    return image