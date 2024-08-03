#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This modules contains different utilities  that are used across different modules in pyaesthetics.

Created on Fri Aug 2 10:51:17 2024

@author: Giulio Gabrieli (gack94@gmail.com).com)
"""

import os #to handle filesystem files
import cv2 #for image manipulation
import numpy as np #numerical computation
import pandas as pd 

def sRGB2RGB(img):
    """ this function converts a sRGB img to linear RGB values.
    
        It loops through each pixel, and apply a conversion to pass from sRGB to linear RGB value.
        
    
        :param img: image to analyze, in sRGB
        :type img: numpy.ndarray
        :return: image to analyze, in RGB
        :rtyipe: numpy.ndarray
    """

    img = img.flatten()
    def converter(p):
        if(p < 0.04045):
            return(p/3294.6)
        else:
            return((((p/255) + 0.055) / 1.055)**2.4)

    newimg = pd.Series(img).apply(converter).to_numpy()
    return(newimg)
###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
""" For debug purposes."""


if __name__ == "__main__":
    pass