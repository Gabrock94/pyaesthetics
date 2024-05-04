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

###############################################################################
#                                                                             #
#                              Saturation                                     #
#                                                                             #
###############################################################################

""" Thìs sections handles the computation of the saturation of an image. """


def saturation(img):
    """This function evaluates the saturationof an image:


    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: saturation
    :rtype: float
    """

    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) / 255
    saturation = img_hsv[:, :, 1].mean()

    return saturation


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
        print(source, saturation(img))
