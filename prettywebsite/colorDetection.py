#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an entrypoint for automatic analysis of a website. 

Created on Mon Apr 16 22:40:46 2018

@author: giulio
"""

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
###############################################################################
#                                                                             #
#                  This section handles color recogntion                      #
#                                                                             #
###############################################################################

def getColorsW3C(img,plot=False):
    """ This functions is used to get a simplified color palette (W3C siteens basic colors).
        
        F = 255
        C0 = 192
        80 = 128
    
        :param img: image to analyze in RGB
        :type img: numpy.ndarray
        :param plot: whether to plot or not the results
        :type plot: boolean
    """
    
    #Defintion of the sixteens basic colors range
    colors = {"Aqua" : "00FFFF",
              "Black": "000000",
              "Blue" : "0000FF",
              "Fuchsia" : "FF00FF",
              "Gray": "808080",
              "Green": "008000",
              "Lime" : "00FF00",
              "Maroon": "800000",
              "Navy" : "000080",
              "Olive" : "808000",
              "Purple" : "800080",
              "Red" : "FF0000",
              "Silver" : "C0C0C0",
              "Teal" : "008080",
              "White" : "FFFFFF",
              "Yellow" : "FFFF00"}
    #Conversone Pixel RGB to HEX
    #Maybe worth superdownsampling (100 x 200)
    img = cv2.resize(img,(200,100),interpolation=cv2.INTER_CUBIC)
    plt.figure()
    plt.imshow(img)
    plt.show()
    colorscheme = []
    return(colorscheme)
    
if(__name__=='__main__'):
    
    basepath = os.path.dirname(os.path.realpath(__file__)) #This get the basepath of the script
    datafolder = basepath+"/../share/data/" #set the data path in order to use sample images
    sampleImg = datafolder + "81.png" #path to a sample image
    img = cv2.imread(sampleImg)
    histogram = [int(x) for x in cv2.calcHist([img],[0],None,[256],[0,256])]
    plt.imshow(img)
    plt.figure()
    img = cv2.resize(img,(200,100),interpolation=cv2.INTER_CUBIC)
    plt.figure()
    plt.imshow(img)
    plt.show()
    #plt.plot(histogram)
    #colors = getColorsW3C(img,plot=True)
    #print("Color scheme of the image is:",colors)