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
    """Compute general info of an image """
    image, shape = facial_landmark[0], facial_landmark[1]
    print("Doing compute_statistics")
    d = Image.fromarray(image)
    image = np.asarray(d)
    height, width = image.shape[:2]

    shape = shape.tolist()
    for i, j in enumerate(shape):
        shape[i] = (j[0], j[1])

    return image, d, shape, height, width

def draw_curve(points, debug):
    """given face feature points, interpolate a smooth cubic curve which passes all the points (makeup region boundary curve) """
    x_pts = []
    y_pts = []
    curvex = []
    curvey = []
    debug += 1
    for point in points:
        x_pts.append(point[0])
        y_pts.append(point[1])
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

def get_boundary_points(x, y):
    """ obtain all boundary coordinates of the makeup region """
    tck, u = interpolate.splprep([x, y], s=0, per=1)
    unew = np.linspace(u.min(), u.max(), 1000)
    xnew, ynew = interpolate.splev(unew, tck, der=0)
    tup = c_[xnew.astype(int), ynew.astype(int)].tolist()
    coord = list(set(tuple(map(tuple, tup))))
    coord = np.array([list(elem) for elem in coord])
    return np.array(coord[:, 0], dtype=np.int32), np.array(coord[:, 1], dtype=np.int32)

def get_interior_points(x, y):
    """ obtain all interior coordinates of the makeup region """
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

def apply_color(img, intensity, r, g, b, height, width):
    """ apply the makeup onto the region with the rgb values """
    val = color.rgb2lab((img / 255.)).reshape(width * height, 3)
    L, A, B = mean(val[:, 0]), mean(val[:, 1]), mean(val[:, 2])
    L1, A1, B1 = color.rgb2lab(np.array((r / 255., g / 255., b / 255.)).reshape(1, 1, 3)).reshape(3, )
    ll, aa, bb = (L1 - L) * intensity, (A1 - A) * intensity, (B1 - B) * intensity
    val[:, 0] = np.clip(val[:, 0] + ll, 0, 100)
    val[:, 1] = np.clip(val[:, 1] + aa, -127, 128)
    val[:, 2] = np.clip(val[:, 2] + bb, -127, 128)

    img = color.lab2rgb(val.reshape(height, width, 3)) * 255
    return img

def smoothen(img_copy, img, height, width, x, y):
    """ blend the makeup slightly with the background image to make it less unnatural """
    imgBase = zeros((height, width))
    cv2.fillConvexPoly(imgBase, np.array(c_[x, y], dtype='int32'), 1)
    imgMask = cv2.GaussianBlur(imgBase, (51, 51), 0)
    imgBlur3D = np.ndarray([height, width, 3], dtype='float')
    imgBlur3D[:, :, 0] = imgMask
    imgBlur3D[:, :, 1] = imgMask
    imgBlur3D[:, :, 2] = imgMask
    img_copy = (imgBlur3D * img * 0.85 + (1 - imgBlur3D * 0.90) * img_copy).astype('uint8')
    return img_copy


