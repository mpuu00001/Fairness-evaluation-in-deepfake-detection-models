"""
General functions for single_makeup

author: Nyee Thoang Lim

references:
https://github.com/hiteshvaidya/Applying-Face-Makeup
https://github.com/TheMathWizard/Face-Makeup-by-Example
https://github.com/hriddhidey/visage/blob/ac58ccd95c832b34ffec61318093e3901539f988/visage/apply_makeup.py#L239
"""

import cv2
from pylab import *
from scipy import interpolate
from skimage import color
import facial_landmark
from PIL import Image

def compute_statistics(image, facial_landmark):
    image, shape = facial_landmark[0], facial_landmark[1]

    d = Image.fromarray(image)
    image = np.asarray(d)
    height, width = image.shape[:2]

    shape = shape.tolist()
    for i, j in enumerate(shape):
        shape[i] = (j[0], j[1])

    return image, d, shape, height, width

def apply_color(img, intensity, r, g, b, height, width):
    if intensity > 1 or intensity < 0:
        # print("Invalid intensity value")
        intensity = 0.5

    val = color.rgb2lab((img / 255.)).reshape(width * height, 3)
    L, A, B = mean(val[:, 0]), mean(val[:, 1]), mean(val[:, 2])
    L1, A1, B1 = color.rgb2lab(np.array((r / 255., g / 255., b / 255.)).reshape(1, 1, 3)).reshape(3, )
    ll, aa, bb = (L1 - L) * intensity, (A1 - A) * intensity, (B1 - B) * intensity
    val[:, 0] = np.clip(val[:, 0] + ll, 0, 100)
    val[:, 1] = np.clip(val[:, 1] + aa, -127, 128)
    val[:, 2] = np.clip(val[:, 2] + bb, -127, 128)

    img = color.lab2rgb(val.reshape(height, width, 3)) * 255
    return img

def get_boundary_points(x, y):

    try:
        if type(x).__module__ != np.__name__:
            raise TypeError
    except TypeError:
        # print("x input shall be numpy")
        x = np.array(x)

    try:
        if type(y).__module__ != np.__name__:
            raise TypeError
    except TypeError:
        # print("y input shall be numpy")
        y = np.array(y)

    if len(x) != len(y):
        print("x length shall be equal to y length")
        return

    tck, u = interpolate.splprep([x, y], s=0, per=1)
    unew = np.linspace(u.min(), u.max(), 1000)
    xnew, ynew = interpolate.splev(unew, tck, der=0)
    tup = c_[xnew.astype(int), ynew.astype(int)].tolist()
    coord = list(set(tuple(map(tuple, tup))))
    coord = np.array([list(elem) for elem in coord])
    return np.array(coord[:, 0], dtype=np.int32), np.array(coord[:, 1], dtype=np.int32)

def get_interior_points(x, y):

    try:
        if type(x).__module__ != np.__name__:
            raise TypeError
    except TypeError:
        # print("x input shall be numpy")
        x = np.array(x)

    try:
        if type(y).__module__ != np.__name__:
            raise TypeError
    except TypeError:
        # print("y input shall be numpy")
        y = np.array(y)

    if len(x) != len(y):
        print("x length shall be equal to y length")
        return

    intx = []
    inty = []

    def ext(a, b, i):
        a, b = round(a), round(b)
        intx.extend(arange(a, b, 1).tolist())
        inty.extend((ones(b - a) * i).tolist())

    x, y = np.array(x), np.array(y)
    xmin, xmax = amin(x), amax(x)
    xrang = np.arange(xmin, xmax + 1, 1)
    for i in xrang:
        ylist = y[where(x == i)]
        ext(amin(ylist), amax(ylist), i)
    return np.array(intx, dtype=np.int32), np.array(inty, dtype=np.int32)


def smoothen(img_copy, img, height, width, x, y, origin = 'moderate', level = 'light'): # blushes
    try:
        if not isinstance(x, list):
            raise TypeError
    except TypeError:
        # print("x input shall be list")
        x = x.tolist()
        # print(type(x))

    try:
        if not isinstance(y, list):
            raise TypeError
    except TypeError:
        # print("y input shall be list")
        y = y.tolist()
        # print(type(y))

    if len(x) != len(y):
        print("x length shall be equal to y length")
        return

    imgBase = zeros((height, width))
    cv2.fillConvexPoly(imgBase, np.array(c_[x, y], dtype='int32'), 1)
    imgMask = cv2.GaussianBlur(imgBase, (51, 51), 0)
    imgBlur3D = np.ndarray([height, width, 3], dtype='float')
    imgBlur3D[:, :, 0] = imgMask
    imgBlur3D[:, :, 1] = imgMask
    imgBlur3D[:, :, 2] = imgMask
    if origin == 'bright':
        if level == 'light':
            img_copy = (imgBlur3D * img * 0.3 + (1 - imgBlur3D * 0.35) * img_copy).astype('uint8')
        if level == 'medium':
            img_copy = (imgBlur3D * img * 0.5 + (1 - imgBlur3D * 0.55) * img_copy).astype('uint8')
        else:
            img_copy = (imgBlur3D * img * 0.4 + (1 - imgBlur3D * 0.45) * img_copy).astype('uint8')
    elif origin == 'moderate':
        if level == 'light':
            img_copy = (imgBlur3D * img * 0.3 + (1 - imgBlur3D * 0.35) * img_copy).astype('uint8')
        if level == 'medium':
            img_copy = (imgBlur3D * img * 0.6 + (1 - imgBlur3D * 0.65) * img_copy).astype('uint8')
        else:
            img_copy = (imgBlur3D * img * 0.4 + (1 - imgBlur3D * 0.45) * img_copy).astype('uint8')
    else:
        if level == 'light':
            img_copy = (imgBlur3D * img * 0.3 + (1 - imgBlur3D * 0.35) * img_copy).astype('uint8')
        if level == 'medium':
            img_copy = (imgBlur3D * img * 0.4 + (1 - imgBlur3D * 0.45) * img_copy).astype('uint8')
        else:
            img_copy = (imgBlur3D * img * 0.4 + (1 - imgBlur3D * 0.45) * img_copy).astype('uint8')
    return img_copy


def smoothen_lipstick(img_copy, img, height, width, x, y, level = 'light'): # blushes
    imgBase = zeros((height, width))
    cv2.fillConvexPoly(imgBase, np.array(c_[x, y], dtype='int32'), 1)
    imgMask = cv2.GaussianBlur(imgBase, (51, 51), 0)
    imgBlur3D = np.ndarray([height, width, 3], dtype='float')
    imgBlur3D[:, :, 0] = imgMask
    imgBlur3D[:, :, 1] = imgMask
    imgBlur3D[:, :, 2] = imgMask
    if level == 'light':
        img_copy = (imgBlur3D * img * 0.3 + (1 - imgBlur3D * 0.35) * img_copy).astype('uint8')
    if level == 'medium':
        img_copy = (imgBlur3D * img * 0.4 + (1 - imgBlur3D * 0.55) * img_copy).astype('uint8')
    else:
        img_copy = (imgBlur3D * img * 0.6 + (1 - imgBlur3D * 0.65) * img_copy).astype('uint8')
    return img_copy


def smoothen_eyeshadow(img_copy, img, height, width, x, y, origin = 'moderate', level = 'light'):
    imgBase = zeros((height, width))
    cv2.fillConvexPoly(imgBase, np.array(c_[x, y], dtype='int32'), 1)
    imgMask = cv2.GaussianBlur(imgBase, (51, 51), 0)
    imgBlur3D = np.ndarray([height, width, 3], dtype='float')
    imgBlur3D[:, :, 0] = imgMask
    imgBlur3D[:, :, 1] = imgMask
    imgBlur3D[:, :, 2] = imgMask
    if origin == 'bright':
        if level == 'light':
            img_copy = (imgBlur3D * img * 0.1 + (1 - imgBlur3D * 0.15) * img_copy).astype('uint8')
        if level == 'medium':
            img_copy = (imgBlur3D * img * 0.6 + (1 - imgBlur3D * 0.65) * img_copy).astype('uint8')
        else:
            img_copy = (imgBlur3D * img * 0.8 + (1 - imgBlur3D * 0.85) * img_copy).astype('uint8')
    elif origin == 'moderate':
        if level == 'light':
            img_copy = (imgBlur3D * img * 0.1 + (1 - imgBlur3D * 0.15) * img_copy).astype('uint8')
        if level == 'medium':
            img_copy = (imgBlur3D * img * 0.7 + (1 - imgBlur3D * 0.75) * img_copy).astype('uint8')
        else:
            img_copy = (imgBlur3D * img * 0.8 + (1 - imgBlur3D * 0.85) * img_copy).astype('uint8')
    else:
        if level == 'light':
            img_copy = (imgBlur3D * img * 0.2 + (1 - imgBlur3D * 0.25) * img_copy).astype('uint8')
        if level == 'medium':
            img_copy = (imgBlur3D * img * 0.4 + (1 - imgBlur3D * 0.5) * img_copy).astype('uint8')
        else:
            img_copy = (imgBlur3D * img * 0.8 + (1 - imgBlur3D * 0.85) * img_copy).astype('uint8')
    return img_copy


def draw_curve(points, debug):

    try:
        for ele in points:
            if type(ele) != tuple:
                raise TypeError
            if len(ele) != 2:
                raise AssertionError
    except TypeError:
        print("Input shall be tuple. ")
        return
    except AssertionError:
        print("Each tuple shall has exactly 2 elements. ")
        return

    x_pts = []
    y_pts = []
    curvex = []
    curvey = []
    debug += 1
    for point in points:
        x_pts.append(point[0]-.001) if point[0] in x_pts else x_pts.append(point[0])
        y_pts.append(point[1])

    # print("\tx_pts: " + str(x_pts))
    # print("\ty_pts: " + str(y_pts))

    curve = interpolate.interp1d(x_pts, y_pts, 'cubic')

    if debug == 1 or debug == 2:
        for i in np.arange(x_pts[0], x_pts[len(x_pts) - 1] + 1, 1):
            curvex.append(i)
            curvey.append(int(curve(i)))
    else:
        for i in np.arange(x_pts[len(x_pts) - 1] + 1, x_pts[0], 1):
            curvex.append(i)
            curvey.append(int(curve(i)))
    return curvex, curvey
