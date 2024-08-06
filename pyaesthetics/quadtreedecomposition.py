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
import math 

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
    The total number of blocks is stored in `self.nblocks`, while the standardized complexity (number of
    blocks divided by the total possible number of blocks is stored in `self.standardized_complexity`. 
    Standardized complexity may range from 0 to 1 (with one being the highest complexity possible).
    The minSize parameter can be automatically adjusted to the common divisor of image width and height closest 
    to the imputted minSize via the `autoadjust` parameter (default to False). The adjusted `minSize` can be 
    obtained (if `autoadjust` = True) by accessing self.minSize.
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
            plt.xticks([],[])
            plt.yticks([],[])
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
        if std >= minStd and max(h/2, w/2) >= minSize: # Check if std and size thresholds are met
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
            self.nblocks = len(self.blocks)
            self.standardized_complexity = self.nblocks / self.max_n_blocks
            
    def __init__(self, img, minStd, minSize, autoadjust = False):
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
        self.minSize = minSize
        if(autoadjust):
            self.minSize = closest_common_divisor(self.img.shape[0], self.img.shape[1], minSize)
            print('Minimum size has been adjusted automatically. The new minSize is ', self.minSize)
        self.max_n_blocks = self.max_quadtree_leaves(self.img.shape[0], self.img.shape[1], self.minSize)
        self.nblocks = 0
        self.standardized_complexity = 0 
        
        self.quad_tree_decomposition(self.img, 0, 0, minStd, self.minSize) # Start the decomposition

    def max_quadtree_leaves(self, width, height, min_leaf_size):
        """
        Calculate the maximum number of leaves in a quadtree decomposition of an image.
    
        :param width: Width of the image in pixels.
        :type width: int
        :param height: Height of the image in pixels.
        :type height: int
        :param min_leaf_size: Minimum size of each side of a leaf in pixels.
        :type min_leaf_size: int
        :return: Maximum number of leaves in the quadtree decomposition.
        :rtype: int
        """
        
        # Calculate maximum depth for width and height
        depth_width = 1
        while width /2/ 2**depth_width >= min_leaf_size:
            depth_width+=1
            
        
        # Calculate maximum depth for width and height
        depth_height = 1
        while height/2 / 2**depth_height >= min_leaf_size:
            depth_height+=1
        
        return((2**depth_height) * (2**depth_width))

def common_divisors(n, m):
    """
    Find all common divisors of n and m.

    :param n: First number.
    :type n: int
    :param m: Second number.
    :type m: int
    :return: A set of common divisors of n and m.
    :rtype: set
    """
    def get_divisors(x):
        divisors = set()
        for i in range(1, int(x**0.5) + 1):
            if x % i == 0:
                divisors.add(i)
                divisors.add(x // i)
        return divisors

    divisors_n = get_divisors(n)
    divisors_m = get_divisors(m)
    return divisors_n.intersection(divisors_m)

def closest_common_divisor(n, m, k):
    """
    Find the common divisor of n and m that is closest to k.

    :param n: First number.
    :type n: int
    :param m: Second number.
    :type m: int
    :param k: Target value.
    :type k: int
    :return: The common divisor closest to k.
    :rtype: int
    """
    common_divs = common_divisors(n, m)
    closest_divisor = min(common_divs, key=lambda x: abs(x - k))
    return closest_divisor

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

    minStd = 20 #Minimum standard deviation for each block
    minSize = 30 # Minimum size of each block in pixels
    
    imgcolor = cv2.imread(sample_img) # Read the image in color for plotting purposes
    img = cv2.imread(sample_img, 0) # Read the image in grayscale
    
    # Create an instance of the quadTree class and perform decomposition
    mydecomposition = quadTree(img, minStd, minSize, autoadjust=True) 
    mydecomposition.plot() # Visual inspection of the results
    print(len(mydecomposition.blocks), mydecomposition.nblocks, mydecomposition.standardized_complexity)
