import numpy as np


def sRGB2RGB(img: np.ndarray) -> np.ndarray:
    """this function converts a sRGB img to  linear RGB values.

    :param img: image to analyze, in sRGB
    :type img: numpy.ndarray
    :return: image to analyze, in RGB
    :rtyipe: numpy.ndarray
    """
    img = img / 255.0
    mask = img <= 0.04045
    img[mask] /= 12.92
    img[~mask] = ((img[~mask] + 0.055) / 1.055) ** 2.4
    return img
