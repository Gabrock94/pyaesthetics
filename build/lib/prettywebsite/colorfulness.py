#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 16 11:49:45 2018

@author: giulio
"""

import os #to handle filesystem files
import cv2 #for image manipulation
import numpy as np #numerical computation

###############################################################################
#                                                                             #
#                              Colorfulness                                   #
#                                                                             #
###############################################################################
""" Thìs sections handles colorfulness estimation. """

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
    
def colorfulnessHSV(img):
    """ This function evaluates the colorfulness of a picture using the formula described in Yendrikhovskij et al., 1998.
        Input image is first converted to the HSV color space, then the S values are selected.
        Ci is evaluated with a sum of the mean S and its std, as in:
            
        Ci = mean(Si)+ std(Si)
    
        :param img: image to analyze, in RGB
        :type img: numpy.ndarray
        :return: colorfulness index
        :rtype: float
    """
    
    img = cv2.cvtColor(img,cv2.COLOR_RGB2HSV) #this converts the image to the HSV color space
    S = [] #initialize a list
    for row in img: #for each row
        for pixel in row: #for each pixel
            S.append(pixel[1]) #take only the Saturation value
    C = np.mean(S) + np.std(S) #evaluate the colorfulness
    return(C) #return the colorfulness index
    
def colorfulnessRGB(img):
    """ This function evaluates the colorfulness of a picture using Metric 3 described in Hasler & Suesstrunk, 2003.
        Ci is evaluated with as:
            
        Ci =std(rgyb) + 0.3 mean(rgyb)   [Equation Y] 
        std(rgyb) = sqrt(std(rg)^2+std(yb)^2)
        mean(rgyb) = sqrt(mean(rg)^2+mean(yb)^2)
        rg = R - G
        yb = 0.5(R+G) - B
    
        :param img: image to analyze, in RGB
        :type img: numpy.ndarray
        :return: colorfulness index
        :rtype: float
    """
    #First we initialize 3 arrays
    R = []
    G = []
    B = []
    for row in img: #for each 
        for pixel in row: #for each pixelò
            #we append the RGB value to the corrisponding list
            R.append(int(pixel[0]))
            G.append(int(pixel[1]))
            B.append(int(pixel[2]))
            
    rg = [R[x] - G[x] for x in range(0,len(R))] #evaluate rg
    yb = [0.5*(R[x] + G[x]) - B[x] for x in range(0,len(R))] #evaluate yb
    
    stdRGYB = np.sqrt(( float(np.std(rg))**2) + (float(np.std(yb))**2)) #evaluate the std of RGYB
    meanRGYB = np.sqrt(( float(np.mean(rg))**2) + (float(np.mean(yb))**2)) #evaluate the mean of RGYB
    C = stdRGYB + 0.3 * meanRGYB #compute the colorfulness index
    return(C)

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
    print(colorfulnessHSV(img))    
    print(colorfulnessRGB(img))

    