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
        :return: percentage distribution of colors according to the W3C sixteens basic colors
        :rtype: list of shape 16x2, where x[0] is the color name and x[1] the percentage of pixels most similar to that color in the image
    """
    
    #Defintion of the sixteens basic colors range
    colors = {"Aqua" : [0,255,255],
              "Black": [0,0,0],
              "Blue" : [0,0,255],
              "Fuchsia" : [255,0,255],
              "Gray": [128,128,128],
              "Green": [0,128,0],
              "Lime" : [0,255,0],
              "Maroon": [128,0,0],
              "Navy" : [0,0,128],
              "Olive" : [128,128,0],
              "Purple" : [128,0,128],
              "Red" : [255,0,0],
              "Silver" : [192,192,192],
              "Teal" : [0,128,128],
              "White" : [255,255,255],
              "Yellow" : [255,255,0]}
    
    colorscheme = []
    #Conversone Pixel RGB to HEX
    #Maybe worth superdownsampling (100 x 200)
    #img = cv2.resize(img,(200,100),interpolation=cv2.INTER_CUBIC)
    if(plot):
        plt.imshow(img)
    for row in img:
        for pixel in row:
            dists = [abs(int(pixel[0]) - int(colors[c][0])) + abs(int(pixel[1]) -int(colors[c][1])) + abs(int(pixel[2]) - int(colors[c][2])) for c in colors.keys()]
#            print(dists)
            colorscheme.append(list(colors.keys())[dists.index(min(dists))])
    colorscheme = sorted([[c, colorscheme.count(c) / len(colorscheme) * 100 ]for c in colors])
    return(colorscheme)
    
if(__name__=='__main__'):
    basepath = os.path.dirname(os.path.realpath(__file__)) #This get the basepath of the script
    datafolder = basepath+"/../share/data/" #set the data path in order to use sample images
    sampleImg = datafolder + "120.png" #path to a sample image
    img = cv2.imread(sampleImg)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    plt.figure()
    plt.imshow(img)
    plt.show()
    histogram = [int(x) for x in cv2.calcHist([img],[0],None,[256],[0,256])]
    #plt.plot(histogram)
    colors = getColorsW3C(img)
    print("Color scheme of the image is:",colors)