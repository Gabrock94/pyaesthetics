#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to evaluate the brightness of an image.
It includes a converter for sRGB to RGB and evaluation of relative luminance according to
BT.709 and BT.601 standards.

Created on Mon Apr 16 22:40:46 2018
Last edited on Fri Aug 2 11:34:10 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

###############################################################################
#                                                                             #
#                                   Libraries                                 #
#                                                                             #
###############################################################################

import os  # To handle filesystem files
import cv2  # For image manipulation
import numpy as np  # Numerical computation
import pandas as pd

###############################################################################
#                                                                             #
#                              Brightness                                     #
#                                                                             #
###############################################################################

""" This section handles brightness estimation. """
    
def relativeluminance_bt709(img):
    """ 
    This function evaluates the brightness of an image by means of Y, where Y is evaluated as:
            
    Y = 0.7152G + 0.0722B + 0.2126R
    B = mean(Y)
        
    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: mean brightness
    :rtype: float
    """
    # Flatten the image array and reshape it to separate color channels
    img = np.array(img).flatten()
    img = img.reshape(int(len(img) / 3), 3)
    img = np.transpose(img)
    
    # Calculate the mean brightness using BT.709 standard
    B = np.mean(img[0]) * 0.2126 + np.mean(img[1]) * 0.7152 + np.mean(img[2]) * 0.0722
    
    return B  # Return the brightness index

def relativeluminance_bt601(img):
    """ 
    This function evaluates the brightness of an image by means of Y, where Y is evaluated as:
            
    Y = 0.587G + 0.114B + 0.299R
    B = mean(Y)
        
    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: mean brightness
    :rtype: float
    """
    # Flatten the image array and reshape it to separate color channels
    img = np.array(img).flatten()
    img = img.reshape(int(len(img) / 3), 3)
    img = np.transpose(img)
    
    # Calculate the mean brightness using BT.601 standard
    B = np.mean(img[0]) * 0.299 + np.mean(img[1]) * 0.587 + np.mean(img[2]) * 0.114
    
    return B  # Return the brightness index

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################

if __name__ == '__main__':
    import utils  # Importing utility functions
    
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"
    
    # Read and preprocess the sample image
    img = cv2.imread(sample_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img = utils.sRGB2RGB(img)
    
    # Calculate and print brightness using BT.709 and BT.601 standards
    print(relativeluminance_bt709(img))  
    print(relativeluminance_bt601(img))
