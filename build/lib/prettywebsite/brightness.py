#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains function to evaluate the brightness of an image.
It includes a converter for sRGB to RGB, evaluation of relative luminance according to
BT.709 and BT.601


Created on Mon Apr 16 16:01:04 2018

@author: giulio
"""

import os #to handle filesystem files
import cv2 #for image manipulation
import numpy as np #numerical computation

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
    newimg = [] #initialize the new img
    for row in img: #for each row
        thisrow = [] #initialize the row
        for pixel in row: #for each pixel
            thispixel = [] #initialize the pixel
            for value in pixel: #for each value R, G and B
                if(value/255 <= 0.04045): #check it is smaller than the treshold
                    thispixel.append(value/(255*12.92)) #do the conversoni
                else: 
                    thispixel.append((((value/255) + 0.055) / 1.055)**2.4) #do the conversion
            thisrow.append(thispixel) #reconstruct the pixel
        newimg.append(thisrow) #recontruct the row
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
    
    Y = [] #initialize a list
    img = sRGB2RGB(img) #conversion from sRGB to linear RGB
    for row in img: #for each row
        for pixel in row: #for each pixel
            Y.append(0.2126 * pixel[0] + 0.7152 *pixel[1] + 0.0722*pixel[2]) #evaluate Y
    B = np.mean(Y)
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
    
    Y = [] #initialize a list
    img = sRGB2RGB(img) #conversion from sRGB to linear RGB
    for row in img: #for each row
        for pixel in row: #for each pixel
            Y.append(0.299 * pixel[0] + 0.587 *pixel[1] + 0.114*pixel[2]) #evaluate Y
    B = np.mean(Y)
    return(B) #return the brigthness index
###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes."""

if(__name__=='__main__'):
    
    basepath = os.path.dirname(os.path.realpath(__file__)) #This get the basepath of the script
    datafolder = basepath+"/../share/data/" #set the data path in order to use sample images
    img = datafolder + "sample.png"
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    print(relativeLuminance_BT709(img))    
    print(relativeLuminance_BT601(img))