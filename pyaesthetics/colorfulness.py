#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains function to evaluate the colorfulness of an image in both the HSV and RGB color spaces.

Created on Mon Apr 16 11:49:45 2018
Last edited on Fri Aug 2 11:44:12 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

import os #to handle filesystem files
import cv2 #for image manipulation
import numpy as np #numerical computation

###############################################################################
#                                                                             #
#                              Colorfulness                                   #
#                                                                             #
###############################################################################

""" This section handles colorfulness estimation. """

def colorfulness_hsv(img):
    """ 
    This function evaluates the colorfulness of a picture using the formula described in Yendrikhovskij et al., 1998.
    Input image is first converted to the HSV color space, then the S values are selected.
    Ci is evaluated with a sum of the mean S and its std, as in:
        
    Ci = mean(Si) + std(Si)

    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: colorfulness index
    :rtype: float
    """
    
    # Convert the image to the HSV color space
    img = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
    
    # Initialize a list to store the Saturation values
    S = []
    
    # Extract the Saturation value for each pixel
    for row in img:
        for pixel in row:
            S.append(pixel[1])
    
    # Evaluate the colorfulness index
    C = np.mean(S) + np.std(S)
    return C

def colorfulness_rgb(img):
    """ 
    This function evaluates the colorfulness of a picture using Metric 3 described in Hasler & Suesstrunk, 2003.
    Ci is evaluated with as:
        
    Ci = std(rgyb) + 0.3 mean(rgyb)   [Equation Y] 
    std(rgyb) = sqrt(std(rg)^2 + std(yb)^2)
    mean(rgyb) = sqrt(mean(rg)^2 + mean(yb)^2)
    rg = R - G
    yb = 0.5(R + G) - B

    :param img: image to analyze, in RGB
    :type img: numpy.ndarray
    :return: colorfulness index
    :rtype: float
    """
    
    # Initialize lists to store the RGB values
    R = []
    G = []
    B = []
    
    # Extract the RGB values for each pixel
    for row in img:
        for pixel in row:
            R.append(int(pixel[0]))
            G.append(int(pixel[1]))
            B.append(int(pixel[2]))
    
    # Evaluate rg and yb
    rg = [R[x] - G[x] for x in range(len(R))]
    yb = [0.5 * (R[x] + G[x]) - B[x] for x in range(len(R))]
    
    # Compute the standard deviation and mean of rgyb
    stdRGYB = np.sqrt((np.std(rg) ** 2) + (np.std(yb) ** 2))
    meanRGYB = np.sqrt((np.mean(rg) ** 2) + (np.mean(yb) ** 2))
    
    # Compute the colorfulness index
    C = stdRGYB + 0.3 * meanRGYB
    return C

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes."""

if __name__ == '__main__':
    
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"
    
    # Read and convert the image
    img = cv2.imread(sample_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Print the colorfulness indices
    print(colorfulness_hsv(img))    
    print(colorfulness_rgb(img))
