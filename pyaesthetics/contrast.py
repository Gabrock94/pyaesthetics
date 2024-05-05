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
from PIL.Image import Image as PilImage

###############################################################################
#                                                                             #
#                              Brightness                                     #
#                                                                             #
###############################################################################

""" Thìs sections handles brigthness estimation. """


def contrast_rms(img: PilImage):
    """This function evaluates the RMS contrast of an image:


    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: RMS contrast
    :rtype: float
    """
    assert img.mode == "RGB", "Image must be in RGB mode"

    img_arr = np.array(img)
    img_grey = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)
    img_grey = img_grey / 255.0
    contrast = img_grey.std()

    # should be the same as:
    # img_s = img_grey - img_grey.mean()
    # img_s = img_s**2
    # contrast2 = np.sqrt(img_s.sum() / (img_s.shape[0] * img_s.shape[1]))
    # print(contrast, contrast2)

    return contrast


def contrast_michelson(img: PilImage):
    """This function evaluates the Michelson contrast of an image:


    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: Michelson contrast
    :rtype: float
    """
    assert img.mode == "RGB", "Image must be in RGB mode"

    img_arr = np.array(img)
    Y = cv2.cvtColor(img_arr, cv2.COLOR_RGB2YUV)[:, :, 0]

    # compute min and max of Y
    minY = float(np.min(Y))
    maxY = float(np.max(Y))
    # compute contrast
    contrast = (maxY - minY) / (maxY + minY)

    return contrast
