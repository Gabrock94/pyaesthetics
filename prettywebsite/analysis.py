#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an entrypoint for automatic analysis of a website. 

Created on Mon Apr 16 22:40:46 2018

@author: giulio
"""

import os
import cv2
import quadTreeDecomposition
import colorfulness
import brightness
import symmetry
import matplotlib.pyplot as plt

###############################################################################
#                                                                             #
#                      Quadratic Tree Decomposition                           #
#                                                                             #
###############################################################################

def analyzeWebsite(pathToImg,resize=True, newSize=(600,400),minStd = 10, minSize = 20):
    resultdict = {}
    imageColor = cv2.imread(pathToImg)
    imageBW = cv2.imread(pathToImg,0)
    if(resize):
        imageBW = cv2.resize(imageBW,newSize,interpolation=cv2.INTER_CUBIC)
        imageColor = cv2.resize(imageColor,newSize,interpolation=cv2.INTER_CUBIC)
    
#    resultdict["brightness_BT709"] = brightness.relativeLuminance_BT709(imageColor)
#    resultdict["brightness_BT601"] = brightness.relativeLuminance_BT601(imageColor)
    resultdict["VC_quadTree"] = len(quadTreeDecomposition.quadTree(imageBW,minStd,minSize).blocks)
    resultdict["VC_weight"] = os.stat(pathToImg).st_size
    resultdict["Symmetry_QTD"] = symmetry.getSymmetry(imageBW,minStd,minSize)
    resultdict["Colorfulness_HSV"] = colorfulness.colorfulnessHSV(imageColor)
    resultdict["Colorfulness_RGB"] = colorfulness.colorfulnessRGB(imageColor)
    return(resultdict)

if(__name__=='__main__'):
    
    basepath = os.path.dirname(os.path.realpath(__file__)) #This get the basepath of the script
    datafolder = "/".join(basepath.split("/")[:-1])+"/data/" #set the data path in order to use sample images
    sampleImg = datafolder + "sample.png" #path to a sample image
    
    results = analyzeWebsite(sampleImg)
    print(results)