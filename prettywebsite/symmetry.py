#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to compute the degree of symmetry of an image.
- Symmetry by QuadTree Decomposition

Created on Mon Apr 16 11:49:45 2018

@author: giulio
"""

import os #to handle filesystem files
import cv2 #for image manipulation
import numpy as np
import matplotlib.pyplot as plt #for data visualization
import matplotlib.patches as patches #for legends and rectangle drawing in QTD
import quadTreeDecomposition
###############################################################################
#                                                                             #
#                                  Symmetry                                   #
#                                                                             #
###############################################################################
""" Thìs sections handles Quadratic Tree Decomposition. """


def getSymmetry(img,minStd,minSize,plot=False):
    """ This function returns the degree of symmetry (0-100) between the left and right side of an image 
    
    :param img: img to analyze
    :type img: numpy.ndarray
    :minStd: Std threshold for subsequent splitting
    :type minStd: int
    :minSize: Size threshold for subsequent splitting, in pixel
    :type minStd: int
    :return: degree of vertical symmetry
    :rtype: float
    """
    h,w = img.shape
    if(h%2 != 0):
        img = img[:-1,:]
    if(w%2 != 0):
        img = img[:,:-1]
        
    left = img[0:,0:int(w/2)]
    right = np.flip(img[0:,int(w/2):],1)
    left = quadTreeDecomposition.quadTree(left,minStd,minSize)
    right = quadTreeDecomposition.quadTree(right,minStd,minSize)
    if(plot):
        left.plot()
        right.plot()
    counter = 0
    tot =  (len(right.blocks) + len(left.blocks))
    for block in right.blocks:
        for block2 in left.blocks:
            if(block[0:4] == block2[0:4]):
                counter+=1
    return(counter /tot * 200)
    
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
    minStd = 15 #min STD of each block
    minSize = 40 #min size of each block    
    imgcolor = cv2.imread(img) #read the image in color for plotting purposes
    img = cv2.imread(img,0) #read the image in B/W
    
    #Symmetry using QT
    h,w = img.shape
    print(getSymmetry(img,minSize,minStd,plot=True))