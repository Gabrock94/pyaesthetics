#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains function to evaluate the saturation of an image.

@author: Giulio Gabrieli
"""

###############################################################################
#                                                                             #
#                                   Libraries                                 #
#                                                                             #
###############################################################################

import cv2  # for image manipulation
import numpy as np
from PIL.Image import Image as PilImage

###############################################################################
#                                                                             #
#                              Saturation                                     #
#                                                                             #
###############################################################################

""" Thìs sections handles the computation of the saturation of an image. """


def get_saturation(img: PilImage) -> float:
    """This function evaluates the saturationof an image:


    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: saturation
    :rtype: float
    """
    assert img.mode == "RGB", "Image must be in RGB mode"
    img_arr = np.array(img)
    img_hsv = cv2.cvtColor(img_arr, cv2.COLOR_RGB2HSV)
    img_hsv = np.divide(img_hsv, 255)
    saturation = img_hsv[:, :, 1].mean()

    return saturation.item()
