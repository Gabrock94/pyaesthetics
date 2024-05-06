"""
This module contains function to evaluate the colorfulness of an image in both the HSV and RGB color spaces.

@author: Giulio Gabrieli
"""

from typing import Union

import cv2  # for image manipulation
import numpy as np  # numerical computation
from PIL.Image import Image as PilImage

###############################################################################
#                                                                             #
#                              Colorfulness                                   #
#                                                                             #
###############################################################################

""" Thìs sections handles colorfulness estimation. """


def get_colorfulness_hsv(img: PilImage) -> float:
    """This function evaluates the colorfulness of a picture using the formula described in Yendrikhovskij et al., 1998.
    Input image is first converted to the HSV color space, then the S values are selected.
    Ci is evaluated with a sum of the mean S and its std, as in:

    Ci = mean(Si)+ std(Si)

    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: colorfulness index
    :rtype: float
    """
    assert img.mode == "RGB", "Image must be in RGB mode"

    img_arr = np.array(img)
    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2HSV)

    S = []  # initialize a list
    for row in img_arr:  # for each row
        for pixel in row:  # for each pixel
            S.append(pixel[1])  # take only the Saturation value
    C = np.mean(S) + np.std(S)  # evaluate the colorfulness
    return C.item()  # return the colorfulness index


def get_colorfulness_rgb(img: PilImage) -> float:
    """This function evaluates the colorfulness of a picture using Metric 3 described in Hasler & Suesstrunk, 2003.
    Ci is evaluated with as:

    Ci =std(rgyb) + 0.3 mean(rgyb)   [Equation Y]
    std(rgyb) = sqrt(std(rg)^2+std(yb)^2)
    mean(rgyb) = sqrt(mean(rg)^2+mean(yb)^2)
    rg = R - G
    yb = 0.5(R+G) - B

    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: colorfulness index
    :rtype: float
    """
    assert img.mode == "RGB", "Image must be in RGB mode"

    img_arr = np.array(img)

    # First we initialize 3 arrays
    R = []
    G = []
    B = []
    for row in img_arr:  # for each
        for pixel in row:  # for each pixelò
            # we append the RGB value to the corrisponding list
            R.append(int(pixel[0]))
            G.append(int(pixel[1]))
            B.append(int(pixel[2]))

    rg = [R[x] - G[x] for x in range(0, len(R))]  # evaluate rg
    yb = [0.5 * (R[x] + G[x]) - B[x] for x in range(0, len(R))]  # evaluate yb

    stdRGYB = np.sqrt(
        (float(np.std(rg)) ** 2) + (float(np.std(yb)) ** 2)
    )  # evaluate the std of RGYB
    meanRGYB = np.sqrt(
        (float(np.mean(rg)) ** 2) + (float(np.mean(yb)) ** 2)
    )  # evaluate the mean of RGYB
    C = stdRGYB + 0.3 * meanRGYB  # compute the colorfulness index
    return C.item()
