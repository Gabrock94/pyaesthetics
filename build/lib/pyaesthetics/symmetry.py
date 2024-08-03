#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to compute the degree of symmetry of an image.
- Symmetry by QuadTree Decomposition

Created on Mon Apr 16 11:49:45 2018
Last edited on Fri Aug 2 12:05:23 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

import os # to handle filesystem files
import cv2 # for image manipulation
import numpy as np # numerical computation
import matplotlib.pyplot as plt # for data visualization
import matplotlib.patches as patches # for legends and rectangle drawing in QTD

###############################################################################
#                                                                             #
#                                  Symmetry                                   #
#                                                                             #
###############################################################################
""" This section handles Quadratic Tree Decomposition. """

class quadTree:
    """ This class performs a QuadTree decomposition of an image. 
    
        During initialization, QuadTree decomposition is done and results are stored in self.blocks
        as a list containing [x, y, height, width, Std].
        
        To visualize the results, use plot().
    """
    
    def plot(self, edgecolor="red", facecolor="none", linewidth=1):
        """ Generate a graphical representation of the QuadTree decomposition.
        
            :param edgecolor: Color of the rectangles, default is red.
            :type edgecolor: string
            :param facecolor: Color used for rectangle fills, default is none.
            :type facecolor: string
            :param linewidth: Width in px of the rectangles' borders, default is 1.
            :type linewidth: int
            :return: Plot with image and leaves of the QuadTree decomposition.
        """
        plt.figure() # Create a new figure
        fig = plt.imshow(self.img) # Plot the original image
        for block in self.blocks: # For each block of results
            rect = patches.Rectangle((block[0], block[1]), block[3], block[2],
                                     linewidth=linewidth, edgecolor=edgecolor, facecolor=facecolor) # Create a rectangle
            fig.axes.add_patch(rect) # Add it to the plot
            plt.title("QuadTree Decomposition") # Add a title
        plt.show() # Show the plot
        
    def quadTreeDecomposition(self, img, x, y, minStd, minSize):
        """ Perform QuadTree decomposition on an image.
        
            :param img: Image to analyze.
            :type img: numpy.ndarray
            :param x: x-offset of the leaves to analyze.
            :type x: int
            :param y: y-offset of the leaves to analyze.
            :type y: int
            :param minStd: Std deviation threshold for splitting.
            :type minStd: int
            :param minSize: Size threshold for splitting, in pixels.
            :type minSize: int
        """
        h, w = img.shape
        mean, std = cv2.meanStdDev(img)
        mean, std = [int(mean), int(std)]
        if std >= minStd and max(h, w) >= minSize: # If std is above the threshold
            # Decide whether to split along X or Y
            if w >= h: # Split along the X-axis
                w2 = int(w / 2) # Get new width
                img1 = img[0:h, 0:w2] # Create the left subimage
                img2 = img[0:h, w2:] # Create the right subimage
                self.quadTreeDecomposition(img1, x, y, minStd, minSize) # Decompose left subimage
                self.quadTreeDecomposition(img2, x + w2, y, minStd, minSize) # Decompose right subimage
            else: # Split along the Y-axis
                h2 = int(h / 2)
                img1 = img[0:h2, :] # Create the top subimage
                img2 = img[h2:, :] # Create the bottom subimage
                self.quadTreeDecomposition(img1, x, y, minStd, minSize) # Decompose top subimage
                self.quadTreeDecomposition(img2, x, y + h2, minStd, minSize) # Decompose bottom subimage
        else:
            self.blocks.append([x, y, h, w, std]) # Add block to results
            
    def __init__(self, img, minStd, minSize):
        """ Initialize QuadTree decomposition analysis.
        
            :param img: Image to analyze.
            :type img: numpy.ndarray
            :param minStd: Std deviation threshold for splitting.
            :type minStd: int
            :param minSize: Size threshold for splitting, in pixels.
            :type minSize: int
        """
        self.blocks = [] # Initialize results
        self.img = img # Assign the image
        self.params = [minStd, minSize] # Set the parameters
        self.quadTreeDecomposition(img, 0, 0, minStd, minSize) # Start decomposition
        
def getSymmetry(img, minStd, minSize, plot=False):
    """ Returns the degree of symmetry (0-100) between the left and right side of an image.
    
    :param img: Image to analyze.
    :type img: numpy.ndarray
    :param minStd: Std deviation threshold for splitting.
    :type minStd: int
    :param minSize: Size threshold for splitting, in pixels.
    :type minSize: int
    :param plot: Whether to plot the QuadTree decomposition of each half.
    :type plot: bool
    :return: Degree of vertical symmetry.
    :rtype: float
    """
    h, w = img.shape
    if h % 2 != 0:
        img = img[:-1, :] # Crop image to even height
    if w % 2 != 0:
        img = img[:, :-1] # Crop image to even width
        
    left = img[:, :int(w / 2)] # Left half of the image
    right = np.flip(img[:, int(w / 2):], 1) # Right half, flipped horizontally
    left = quadTree(left, minStd, minSize) # Decompose left half
    right = quadTree(right, minStd, minSize) # Decompose right half
    
    if plot:
        left.plot() # Plot decomposition of left half
        right.plot() # Plot decomposition of right half
        
    counter = 0
    total = len(right.blocks) + len(left.blocks)
    
    # Count matching blocks between left and right halves
    for block in right.blocks:
        for block2 in left.blocks:
            if block[0:4] == block2[0:4]:
                counter += 1
                
    return (counter / total * 200) # Return degree of symmetry

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes. """

if __name__ == '__main__':
    basepath = os.path.dirname(os.path.realpath(__file__)) # Get the basepath of the script
    datafolder = basepath + "/../share/data/" # Set the data path for sample images
    img = datafolder + "jade.png"
    minStd = 5 # Min STD of each block
    minSize = 20 # Min size of each block
    imgcolor = cv2.imread(img) # Read the image in color for plotting purposes
    img = cv2.imread(img, 0) # Read the image in grayscale
    # Symmetry using QuadTree decomposition
    h, w = img.shape
    print(getSymmetry(img, minSize, minStd, plot=True)) # Print the degree of symmetry
