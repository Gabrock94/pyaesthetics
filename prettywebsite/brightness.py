#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
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
    
        :param img: image to analyze, in sRGB
        :type img: numpy.ndarray
        :return: image to analyze, in RGB
        :rtyipe: numpy.ndarray
    """
    newimg = []
    for row in img:
        thisrow = [] 
        for pixel in row:
            thispixel = []
            for value in pixel:
                if(value/255 <= 0.04045):
                    thispixel.append(value/(255*12.92))
                else:
                    thispixel.append((((value/255) + 0.055) / 1.055)**2.4)
            thisrow.append(thispixel)
        newimg.append(thisrow)
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
    datafolder = "/".join(basepath.split("/")[:-1])+"/data/"
    img = datafolder + "sample.png"
    img = cv2.imread(img)
    print(relativeLuminance_BT709(img))    
    print(relativeLuminance_BT601(img))

    