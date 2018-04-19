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
def getFaces(img,plot=False):
    """ This functions uses CV2 to get the faces in a pciture.
    
        :param img: image to analyze in RGB
        :type img: numpy.ndarray
        :param plot: whether to plot or not the results
        :type plot: boolean
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    frontalface_cascade = cv2.CascadeClassifier(os.path.join(os.path.dirname(__file__), '../share/data/haarcascade_frontalface_default.xml'))
    faces = frontalface_cascade.detectMultiScale(img, 1.3, 5)
    if(plot):
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
            plt.imshow(img)

    return(faces)
    
if(__name__=='__main__'):
    
    basepath = os.path.dirname(os.path.realpath(__file__)) #This get the basepath of the script
    datafolder = basepath+"/../share/data/" #set the data path in order to use sample images
    sampleImg = datafolder + "81.png" #path to a sample image
    img = cv2.imread(sampleImg)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    faces = getFaces(img,plot=True)
    print("Number of faces in the picture is:",len(faces))