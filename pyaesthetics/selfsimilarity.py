#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to compute the degree of selfsimilarity of an image.
- Self Similarity is evaluated using the PHOG method proposed in Amirshahi, S. A., Koch, M., Denzler, J., & Redies, C. (2012, February). PHOG analysis of self-similarity in aesthetic images. In Human Vision and Electronic Imaging XVII (Vol. 8291, p. 82911J). International Society for Optics and Photonics.

Created on Mon Oct 18 17:22:45 2021

@author: giulio
"""


import os #to handle filesystem files
import cv2
from matplotlib import image #for image manipulation
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage.transform import resize

###############################################################################
#                                                                             #
#                               Self Similarity                               #
#                                                                             #
###############################################################################

class selfsimilarity:
    """ This function returns the degree of self similarity (0-1) of an image 
    
    :param img: img to analyze
    :type img: numpy.ndarray
    :maxlevel: Maximum number of level to analyze.
    :type minStd: int
    :return: degree of self similarity
    :rtype: float
    """
    def getHogs(self, img):
        h,w,_ = img.shape
        Il, Ia, Ib = cv2.split(img)
        gIl, gIa, gIb = np.gradient(Il, edge_order = 2, axis=0), np.gradient(Ia, edge_order = 2, axis=0), np.gradient(Ib, edge_order = 2, axis=0)
        gIl = np.array(gIl).flatten()
        gIa = np.array(gIa).flatten()
        gIb = np.array(gIb).flatten()
        G = np.amax(np.transpose([gIl, gIa, gIb]),1)
        G = np.reshape(G, (h,w))
        hogs = hog(G, orientations=16)
        hogs = (hogs + min(hogs)) / sum(hogs + min(hogs)) #normalize so that sum is 1, this is ground
        return(hogs)

    def getSimilarity(self, img, groundhogs, parenthogs, level):
        #divide the image in four
        h, w, _ = img.shape
        w2 = int(w/2)
        h2 = int(h/2)
        img1, img2, img3, img4 = img[:, 0:h2, 0:w2], img[:, 0:h2, w2:w], img[:, h2:h, 0:w2], img[:, h2:h,w2:w]
        hogs1, hogs2, hogs3, hogs4 = self.getHogs(img1), self.getHogs(img2), self.getHogs(img3), self.getHogs(img4)
        
        print(sum(np.amin(np.transpose([hogs1, parenthogs]), 1)))
        print(sum(np.amin(np.transpose([hogs2, parenthogs]), 1)))
        print(sum(np.amin(np.transpose([hogs3, parenthogs]), 1)))
        print(sum(np.amin(np.transpose([hogs4, parenthogs]), 1)))

        if(level <= self.maxlevel):
            pass

    def __init__(self,img,maxlevel=4):
        self.image_LAB = cv2.cvtColor(img, cv2.COLOR_BGR2LAB) #convert image to LAB Colorspace
        self.maxlevel = maxlevel
        hogs = self.getHogs(self.image_LAB)

        self.getSimilarity(self.image_LAB, hogs, hogs, 1)


###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes."""

if(__name__=='__main__'):   
    img = "/home/giulio/Repositories/PrettyWebsite/prettywebsite/sample.jpg" #path to a sample image
    img = cv2.imread(img) #read the image in color for plotting purposes
    selfsimilarity(img)