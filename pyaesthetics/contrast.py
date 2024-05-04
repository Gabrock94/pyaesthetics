#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains function to evaluate the contrast of an image using either
RMS contrast or Michelson contrast.

@author: Giulio Gabrieli
"""

###############################################################################
#                                                                             #
#                                   Libraries                                 #
#                                                                             #
###############################################################################

import cv2  # for image manipulation
import numpy as np  # numerical computation
import pandas as pd

###############################################################################
#                                                                             #
#                              Brightness                                     #
#                                                                             #
###############################################################################

""" Thìs sections handles brigthness estimation. """


def sRGB2RGB(img):
    """this function converts a sRGB img to  linear RGB values.

    It loops through each pixel, and apply a conversion to pass from sRGB to linear RGB value.


    :param img: image to analyze, in sRGB
    :type img: numpy.ndarray
    :return: image to analyze, in RGB
    :rtyipe: numpy.ndarray
    """

    img = img.flatten()

    def converter(p):
        if p < 0.04045:
            return p / 3294.6
        else:
            return (((p / 255) + 0.055) / 1.055) ** 2.4

    newimg = pd.Series(img).apply(converter).to_numpy()
    return newimg


def contrast_RMS(img):
    """This function evaluates the RMS contrast of an image:


    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: RMS contrast
    :rtype: float
    """

    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) / 255
    contrast = img_grey.std()

    # should be the same as:
    # img_s = img_grey - img_grey.mean()
    # img_s = img_s**2
    # contrast2 = np.sqrt(img_s.sum() / (img_s.shape[0] * img_s.shape[1]))
    # print(contrast, contrast2)

    return contrast


def contrast_Michelson(img):
    """This function evaluates the Michelson contrast of an image:


    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: Michelson contrast
    :rtype: float
    """

    Y = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:, :, 0]

    # compute min and max of Y
    minY = float(np.min(Y))
    maxY = float(np.max(Y))
    # compute contrast
    contrast = (maxY - minY) / (maxY + minY)

    return contrast


###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################

if __name__ == "__main__":
    for source in [
        "/home/giulio/Repositories/pyaesthetics/share/data/800px-Multi-color_leaf_without_saturation.jpg",
        "/home/giulio/Repositories/pyaesthetics/share/data/800px-Multi-color_leaf_with_saturation.jpg",
    ]:
        img = source

        img = cv2.imread(img)
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        # img = sRGB2RGB(img)
        print(contrast_RMS(img))
        print(contrast_Michelson(img))
