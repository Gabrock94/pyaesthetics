#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This file contains a class and functions to perform a Quadratic Tree decomposition
of an image and to visually inspect it.

Created on Mon Apr 16 11:49:45 2018
Last edited on Fri Aug 2 11:46:24 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

import os # to handle filesystem files
import cv2 # for image manipulation
import numpy as np # numerical computation
import matplotlib.pyplot as plt # for data visualization
import matplotlib.patches as patches # for drawing rectangles in the plot

###############################################################################
#                                                                             #
#                      Quadratic Tree Decomposition                           #
#                                                                             #
###############################################################################
""" This section handles Quadratic Tree Decomposition. """

class quadTree:
    """ 
    This class performs a QuadTree decomposition of an image. 
    
    During initialization, the QuadTree decomposition is done and results are stored in `self.blocks` 
    as a list containing [x, y, height, width, Std]. To visualize the results, use the `plot()` method.
    """
    
    def plot(self, edgecolor="red", facecolor="none", linewidth=1):
        """ 
        Generate a graphical representation of the QuadTree decomposition. 
        
        :param edgecolor: Color of the rectangle edges, default is red
        :type edgecolor: string
        :param facecolor: Color used for rectangle fills. Default is none.
        :type facecolor: string
        :param linewidth: Width of the rectangles' borders in pixels. Default is 1.
        :type linewidth: int
        :return: Plot with image and leaves of the QuadTree Decomposition
        """
        plt.figure() # Create a new figure
        fig = plt.imshow(self.img) # Plot the original image
        for block in self.blocks: # For each block of results
            rect = patches.Rectangle(
                (block[0], block[1]), # Position (x, y) of the rectangle
                block[3], # Width of the rectangle
                block[2], # Height of the rectangle
                linewidth=linewidth, # Border width
                edgecolor=edgecolor, # Border color
                facecolor=facecolor # Fill color
            )
            fig.axes.add_patch(rect) # Add rectangle to the plot
            plt.title("QuadTree Decomposition") # Set the plot title
        plt.show() # Display the plot
        
    def quad_tree_decomposition(self, img, x, y, minStd, minSize):
        """ 
        Evaluate the mean and standard deviation of an image block, and decide whether to perform 
        further splits of the block.

        :param img: Image to analyze
        :type img: numpy.ndarray
        :param x: X offset of the block to analyze
        :type x: int
        :param y: Y offset of the block to analyze
        :type y: int
        :param minStd: Standard deviation threshold for subsequent splitting
        :type minStd: int
        :param minSize: Size threshold for subsequent splitting, in pixels
        :type minSize: int
        """
        h, w = img.shape # Get the height and width of the image
        mean, std = cv2.meanStdDev(img) # Compute the mean and standard deviation
        mean, std = [int(mean.item()), int(std.item())]  
        
        if std >= minStd and max(h, w) >= minSize: # Check if std and size thresholds are met
            # Decide whether to split along X or Y axis
            if w >= h: # Split along the X axis
                w2 = int(w / 2) # Compute new width
                img1 = img[0:h, 0:w2] # Create the left subimage
                img2 = img[0:h, w2:] # Create the right subimage
                # Recursively perform QuadTree decomposition
                self.quad_tree_decomposition(img1, x, y, minStd, minSize)
                self.quad_tree_decomposition(img2, x + w2, y, minStd, minSize)
            else: # Split along the Y axis
                h2 = int(h / 2) # Compute new height
                img1 = img[0:h2, 0:] # Create the upper subimage
                img2 = img[h2:, 0:] # Create the lower subimage
                # Recursively perform QuadTree decomposition
                self.quad_tree_decomposition(img1, x, y, minStd, minSize)
                self.quad_tree_decomposition(img2, x, y + h2, minStd, minSize)
        else:
            # Add the block to the results if it does not meet the splitting criteria
            self.blocks.append([x, y, h, w, std])
            
    def __init__(self, img, minStd, minSize):
        """ 
        Initialize the QuadTree decomposition analysis. 
        
        :param img: Image to analyze
        :type img: numpy.ndarray
        :param minStd: Standard deviation threshold for subsequent splitting
        :type minStd: int
        :param minSize: Size threshold for subsequent splitting, in pixels
        :type minSize: int
        """
        self.blocks = [] # Initialize the results list
        self.img = img # Assign the image
        self.params = [minStd, minSize] # Set the parameters
        self.quad_tree_decomposition(img, 0, 0, minStd, minSize) # Start the decomposition
        
###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes, this section reads a sample image and performs QuadTree decomposition. """

if __name__ == '__main__':
    # Path to a sample image
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"

    minStd = 15 # Minimum standard deviation for each block
    minSize = 40 # Minimum size of each block in pixels
    
    imgcolor = cv2.imread(sample_img) # Read the image in color for plotting purposes
    img = cv2.imread(sample_img, 0) # Read the image in grayscale
    
    # Create an instance of the quadTree class and perform decomposition
    mydecomposition = quadTree(img, minStd, minSize) 
    mydecomposition.plot() # Visual inspection of the results
