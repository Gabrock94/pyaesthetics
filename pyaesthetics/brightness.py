"""
This module contains function to evaluate the brightness of an image.
It includes a converter for sRGB to RGB, evaluation of relative luminance according to
BT.709 and BT.601

@author: Giulio Gabrieli
"""

###############################################################################
#                                                                             #
#                                   Libraries                                 #
#                                                                             #
###############################################################################

import numpy as np
from PIL.Image import Image as PilImage

from pyaesthetics.utils import sRGB2RGB

###############################################################################
#                                                                             #
#                              Brightness                                     #
#                                                                             #
###############################################################################

""" Thìs sections handles brigthness estimation. """


def relative_luminance_bt709(img: PilImage) -> float:
    """This function evaluates the brightness of an image by mean of Y, where Y is evaluated as:

    Y = 0.7152G + 0.0722B + 0.2126R
    B = mean(Y)

    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: mean brightness
    :rtype: float
    """
    assert img.mode == "RGB", "Image must be in RGB mode"

    img_arr = np.array(img)
    img_arr = sRGB2RGB(img_arr)

    img_arr = img_arr.flatten()
    img_arr = img_arr.reshape(int(len(img_arr) / 3), 3)
    img_arr = np.transpose(img_arr)
    return (
        np.mean(img_arr[0]) * 0.2126
        + np.mean(img_arr[1]) * 0.7152
        + np.mean(img_arr[2]) * 0.0722
    )


def relative_luminance_bt601(img: PilImage) -> float:
    """This function evaluates the brightness of an image by mean of Y, where Y is evaluated as:

    Y = 0.587G + 0.114B + 0.299R
    B = mean(Y)

    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: mean brightness
    :rtype: float
    """
    assert img.mode == "RGB", "Image must be in RGB mode"

    img_arr = np.array(img)
    img_arr = sRGB2RGB(img_arr)

    img_arr = img_arr.flatten()
    img_arr = img_arr.reshape(int(len(img_arr) / 3), 3)
    img_arr = np.transpose(img_arr)
    return (
        np.mean(img_arr[0]) * 0.299
        + np.mean(img_arr[1]) * 0.587
        + np.mean(img_arr[2]) * 0.114
    )
