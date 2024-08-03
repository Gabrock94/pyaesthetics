#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to evaluate the contrast of an image using either 
RMS contrast or Michelson contrast.

Created on Wed Apr 10 11:49:45 2018
Last edited on Fri Aug  2 11:46:24 2024
  
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
import pandas as pd # for data manipulation (not used in this script, but imported)

###############################################################################
#                                                                             #
#                              Contrast Estimation                           #
#                                                                             #
###############################################################################

""" This section handles contrast estimation. """

def contrast_rms(img):
    """ 
    This function evaluates the RMS (Root Mean Square) contrast of an image.
    The RMS contrast is calculated as the standard deviation of pixel intensities 
    in the grayscale version of the image.
    
    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: RMS contrast 
    :rtype: float
    """
    
    # Convert the image to grayscale and normalize pixel values to the range [0, 1]
    img_grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) / 255
    
    # Compute the standard deviation of pixel values in the grayscale image
    contrast = img_grey.std()
    
    # Alternative method to compute RMS contrast (commented out for reference)
    # img_s = img_grey - img_grey.mean()
    # img_s = img_s**2
    # contrast2 = np.sqrt(img_s.sum() / (img_s.shape[0] * img_s.shape[1]))
    # print(contrast, contrast2)
    
    return contrast

def contrast_michelson(img):
    """ 
    This function evaluates the Michelson contrast of an image.
    The Michelson contrast is calculated based on the luminance channel (Y) of the YUV color space:
    
    Michelson contrast = (maxY - minY) / (maxY + minY)
    
    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: Michelson contrast
    :rtype: float
    """
    
    # Convert the image to YUV color space and extract the luminance channel (Y)
    Y = cv2.cvtColor(img, cv2.COLOR_BGR2YUV)[:,:,0]

    # Compute the minimum and maximum values of the Y channel
    minY = float(np.min(Y))
    maxY = float(np.max(Y))
    
    # Compute the Michelson contrast
    contrast = (maxY - minY) / (maxY + minY)

    return contrast

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes, this section reads sample images and calculates their contrast. """

if __name__ == '__main__':
    
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"
    
    # Read the image from file
    img = cv2.imread(sample_img)
    
    # Print the RMS and Michelson contrast values for the image
    print("RMS Contrast:", contrast_rms(img))  
    print("Michelson Contrast:", contrast_michelson(img))
