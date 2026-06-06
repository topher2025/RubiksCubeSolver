import numpy as np
import cv2
from time import sleep

from . import util


DEBUG = True


def laplacian(path=None, pimg=None, rimg=None):
    global DEBUG
    image = util.args(path, pimg, rimg)
    if not image:
        return None
    
    lap = cv2.Laplacian(image, cv2.CV_64F)
    lap = cv2.convertScaleAbs(lap)

    if DEBUG:
        cv2.imshow("Original", image)
        cv2.imshow("Laplacian", lap)
        sleep(5)
    
    return lap


def sobel(path=None, pimg=None, rimg=None):
    global DEBUG
    image = util.args(path, pimg, rimg)
    if not image:
        return None
    
    sobelX = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(image, cv2.CV_64F, 0, 1)

    sobelCombined = cv2.bitwise_or(sobelX, sobelY)

    if DEBUG:
        cv2.imshow("Sobel X", sobelX)
        cv2.imshow("Sobel Y", sobelY)
        cv2.imshow("Sobel Combined", sobelCombined)
        sleep(5)


if "__main__" == __name__:
    pass

