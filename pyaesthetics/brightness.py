#!/usr/bin/env python3
# -*- coding: utf-8 -*-
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

import os #to handle filesystem files
import cv2 #for image manipulation
import numpy as np #numerical computation
import pandas as pd 

###############################################################################
#                                                                             #
#                              Brightness                                     #
#                                                                             #
###############################################################################

""" Thìs sections handles brigthness estimation. """

def sRGB2RGB(img):
    """ this function converts a sRGB img to  linear RGB values.
    
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
    
def relativeLuminance_BT709(img):
    """ This function evaluates the brightness of an image by mean of Y, where Y is evaluated as:
            
        Y = 0.7152G + 0.0722B + 0.2126R
        B = mean(Y)
        
        :param img: image to analyze, in RGB
        :type img: numpy.ndarray
        :return: mean brightness
        :rtype: float
    """
    
    img = np.array(img).flatten()
    img = img.reshape(int(len(img)/3),3)
    img = np.transpose(img)
    B = np.mean(img[0]) * 0.2126 + np.mean(img[1]) * 0.7152 + np.mean(img[2]) * 0.0722
    return(B) #return the brigthness index

def relativeLuminance_BT601(img):
    """ This function evaluates the brightness of an image by mean of Y, where Y is evaluated as:
            
        Y = 0.587G + 0.114B + 0.299R
        B = mean(Y)
        
        :param img: image to analyze, in RGB
        :type img: numpy.ndarray
        :return: mean brightness
        :rtype: float
    """
    
    
    img = np.array(img).flatten()
    img = img.reshape(int(len(img)/3),3)
    img = np.transpose(img)
    B = np.mean(img[0]) * 0.299 + np.mean(img[1]) * 0.587 + np.mean(img[2]) * 0.114

    return(B) #return the brigthness index

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
if(__name__=='__main__'):

        img = "/home/giulio/Repositories/pyaesthetics/pyaesthetics/sample.jpg" #path to a sample image

        img = cv2.imread(img)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = sRGB2RGB(img)
        print(relativeLuminance_BT709(img))  
        print(relativeLuminance_BT601(img))