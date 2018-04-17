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
#                      Quadratic Tree Decomposition                           #
#                                                                             #
###############################################################################
def getFaces(img):
    #if(__name__ == "__main__"):
    frontalface_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), '../share/data/haarcascade_frontalface_default.xml'))
    faces = frontalface_cascade.detectMultiScale(img, 1.3, 5)
    return(faces)
    
if(__name__=='__main__'):
    
    basepath = os.path.dirname(os.path.realpath(__file__)) #This get the basepath of the script
    datafolder = "/".join(basepath.split("/")[:-1])+"/data/" #set the data path in order to use sample images
    sampleImg = datafolder + "sample.png" #path to a sample image
    img = cv2.imread(sampleImg)
    imageGrey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = getFaces(imageGrey)
    print("Number of faces in the picture is:",len(faces))