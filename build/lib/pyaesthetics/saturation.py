#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains a function to evaluate the saturation of an image.

Created on Wed Apr 10 11:49:45 2018
Last edited on Fri Aug 2 11:46:24 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

###############################################################################
#                                                                             #
#                                   Libraries                                 #
#                                                                             #
###############################################################################

import os # to handle filesystem files
import cv2 # for image manipulation
import numpy as np # numerical computation
import pandas as pd # (not used in this script, but imported)

###############################################################################
#                                                                             #
#                              Saturation                                     #
#                                                                             #
###############################################################################

""" This section handles the computation of the saturation of an image. """

def saturation(img):
    """ 
    This function evaluates the saturation of an image.
        
    The image is first converted to the HSV color space, then the mean saturation value is computed.
    
    :param img: Image to analyze, in RGB format.
    :type img: numpy.ndarray
    :return: Mean saturation value of the image.
    :rtype: float
    """
    
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV) / 255  # Convert image to HSV color space and normalize to [0, 1]
    saturation = img_hsv[:, :, 1].mean()  # Compute the mean of the Saturation channel
    
    return saturation  # Return the mean saturation value

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes: reads sample images and computes their saturation values. """

if __name__ == '__main__':

    # List of sample image paths to test the saturation function
    for source in [
        "/home/giulio/Repositories/pyaesthetics/share/data/800px-Multi-color_leaf_without_saturation.jpg",
        "/home/giulio/Repositories/pyaesthetics/share/data/800px-Multi-color_leaf_with_saturation.jpg"
    ]:
        img = source  # Path to the image file
        img = cv2.imread(img)  # Read the image
        print(source, saturation(img))  # Print the image path and its saturation value
