import numpy as np
import cv2
from time import sleep

import util


DEBUG = True


def laplacian(path=None, pimg=None, rimg=None):
    global DEBUG
    image = util.args(path, pimg, rimg)
    if image is None:
        return None
    
    lap = cv2.Laplacian(image, cv2.CV_64F)
    lap = cv2.convertScaleAbs(lap)

    if DEBUG:
        print("[DEBUG] Original")
        cv2.imshow("Original", image)
        print("[DEBUG] Laplacian")
        cv2.imshow("Laplacian", lap)
        cv2.waitKey(0)
    
    return lap


def sobel(path=None, pimg=None, rimg=None):
    global DEBUG
    image = util.args(path, pimg, rimg)
    if image is None:
        return None
    
    sobelX = cv2.Sobel(image, cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(image, cv2.CV_64F, 0, 1)

    sobelCombined = cv2.bitwise_or(sobelX, sobelY)

    if DEBUG:
        print("[DEBUG] Original")
        cv2.imshow("Original", image)
        print("[DEBUG] Soble X")
        cv2.imshow("Sobel X", sobelX)
        print("[DEBUG] Soble Y")
        cv2.imshow("Sobel Y", sobelY)
        print("[DEBUG] Soble Combined")
        cv2.imshow("Sobel Combined", sobelCombined)


if "__main__" == __name__:
    if DEBUG:
        print("[DEBUG] Debug active")
    p='/home/to/PycharmProjects/RubiksCubeSolver/tests/images/front_solved_min.jpeg'
    
    laplacian(path=p)

