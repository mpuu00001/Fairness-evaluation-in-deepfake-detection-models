"""
Facial landmarks detection using dlib

author: Nyee Thoang Lim
reference: https://www.pyimagesearch.com/2017/04/03/facial-landmarks-dlib-opencv-python/
"""

import cv2
import dlib
import imutils
from imutils import face_utils


def detect_facial_landmark(image):
    """
    Given a frontal face image, detect the 68 facial landmarks.
    image: a frontal face image
    """

    image = imutils.resize(image, width=500) # enlage the size
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # convert to grayscale
    detector = dlib.get_frontal_face_detector()
    faces = detector(gray, 1)
    print("faces: " + str(faces))

    p = '/Users/muxin/PyCharm/makeup_application/facial_landmarks_detection/shape_predictor_68_face_landmarks.dat' # predictor model
    predictor = dlib.shape_predictor(p)
    shape = predictor(gray, faces[0]) # get facial landmarks
    shape = face_utils.shape_to_np(shape)
    return image, shape
