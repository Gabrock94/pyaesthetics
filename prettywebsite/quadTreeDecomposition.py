#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains class and functions to perform a Quadratic Tree decomposition
of an image and to visually inspect it.

Created on Mon Apr 16 11:49:45 2018

@author: giulio
"""

import os #to handle filesystem files
import cv2 #for image manipulation
import numpy as np
import matplotlib.pyplot as plt #for data visualization
import matplotlib.patches as patches #for legends and rectangle drawing in QTD

###############################################################################
#                                                                             #
#                      Quadratic Tree Decomposition                           #
#                                                                             #
###############################################################################
""" Thìs sections handles Quadratic Tree Decomposition. """

class quadTree:
    """ This class is used to perfrom a QuadTree decomposition of an image. 
    
        During initialization, QuadTree decomposition is done and result are store in self.blocks as a list containing [x,y,height, width,Std].
        
        To visualize the results, use plot().
    """
    
    def plot(self,edgecolor="red", facecolor="none", linewidth = 1):
        """ This function is used to generate a graphical representation of the QuadTree decomposition. 
        
            :param edgecolor: color of the rectangles, default is red
            :type edgecolor: string
            :param facecolor: color used for rectangles fills. Default is none.
            :type facecolor: string
            :param linewidth: width in px of the rectangles' borders. Default is 1.
            :type linewidth:
            :return: plot with image and leaves of the quadTree Decomposition
        """
        plt.figure() #create a new figure
        fig = plt.imshow(self.img) #plot the original image
        for block in self.blocks: #for each block of results
            rect = patches.Rectangle((block[0],block[1]),block[3],block[2],linewidth=linewidth,edgecolor=edgecolor,facecolor=facecolor) #create a red rectangle
            fig.axes.add_patch(rect) #add it to the picture
            plt.title("QuadTree Decomposition") #give it a title
        plt.show() #show the results
        
    def quadTreeDecomposition(self,img,x,y,minStd,minSize):
        """ This function evaluate the mean and std of an image, and decides Whether to perform or not other 2 splits of the leave. 
        
            :param img: img to analyze
            :type img: numpy.ndarray
            :param x: x offset of the leaves to analyze
            :type x: int
            :param Y: Y offset of the leaves to analyze
            :type Y: int
            :minStd: Std threshold for subsequent splitting
            :type minStd: int
            :minSize: Size threshold for subsequent splitting, in pixel
            :type minStd: int
        """
        h,w = img.shape
        mean, std = cv2.meanStdDev(img)
        mean, std = [int(mean),int(std)]
        if(std >= minStd and max(h,w) >= minSize):#if std is > then our threshold:
            #Decide if slip along X or Y
            if(w >= h): #split along the X axis
                w2 = int(w/2) #get the new width
                img1 = img[0:h,0:w2] #create a subimage
                img2 = img[0:h,w2:] #create the second subimage
                self.quadTreeDecomposition(img1,x,y,minStd,minSize) #do the quadtree on image 1
                self.quadTreeDecomposition(img2,x+w2,y,minStd,minSize) #do it on the second
            else: #split Y
                h2 = int(h/2)
                img1 = img[0:h2,0:]
                img2 = img[h2:,0:]
                self.quadTreeDecomposition(img1,x,y,minStd,minSize)
                self.quadTreeDecomposition(img2,x,y+h2,minStd,minSize)
        else:
            self.blocks.append([x,y,h,w,std])
            
    def __init__(self,img,minStd,minSize):
        """ Initialize the quadTree decomposition analysis. 
        
            :param img: img to analyze
            :type img: numpy.ndarray
            :minStd: Std threshold for subsequent splitting
            :type minStd: int
            :minSize: Size threshold for subsequent splitting, in pixel
            :type minStd: int
        """
        self.blocks = [] #intialize th results
        self.img = img #assign the image
        self.params = [minStd,minSize] #set the parameters
        self.quadTreeDecomposition(img,0,0,minStd,minSize) #start the decomposition
        
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
    minStd = 15 #min STD of each block
    minSize = 40 #min size of each block    
    imgcolor = cv2.imread(img) #read the image in color for plotting purposes
    img = cv2.imread(img,0) #read the image in B/W
    
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    mydecomposition = quadTree(img,minStd,minSize) #start the decomposition
    mydecomposition.plot() #visual inspection of the results