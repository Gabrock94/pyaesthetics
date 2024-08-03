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

# Attempt to import internal modules of pyaesthetics, handling both relative and absolute imports
try:
    from . import quadtreedecomposition
    from . import utils
except:
    import quadtreedecomposition
    import utils

###############################################################################
#                                                                             #
#                                  Symmetry                                   #
#                                                                             #
###############################################################################
        
def get_symmetry(img, minStd, minSize, plot=False):
    """ Returns the degree of symmetry (0-100) between the left and right side of an image.
    
    :param img: Image to analyze.
    :type img: numpy.ndarray
    :param minStd: Std deviation threshold for splitting.
    :type minStd: int
    :param minSize: Size threshold for splitting, in pixels.
    :type minSize: int
    :param plot: Whether to plot the QuadTree decomposition of each half.
    :type plot: bool
    :return: Degree of vertical symmetry between 0 and 1.
    :rtype: float
    """
    h, w = img.shape
    if h % 2 != 0:
        img = img[:-1, :] # Crop image to even height
    if w % 2 != 0:
        img = img[:, :-1] # Crop image to even width
        
    left = img[:, :int(w / 2)] # Left half of the image
    right = np.flip(img[:, int(w / 2):], 1) # Right half, flipped horizontally
    left = quadtreedecomposition.quadTree(left, minStd, minSize) # Decompose left half
    right = quadtreedecomposition.quadTree(right, minStd, minSize) # Decompose right half
    
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
                
    return (counter / total * 2) # Return degree of symmetry

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes. """

if __name__ == '__main__':
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"
    
    minStd = 5 # Min STD of each block
    minSize = 20 # Min size of each block
    
    imgcolor = cv2.imread(sample_img) # Read the image in color for plotting purposes
    img = cv2.imread(sample_img, 0) # Read the image in grayscale
    # Symmetry using QuadTree decomposition
    h, w = img.shape
    print(get_symmetry(img, minSize, minStd, plot=True)) # Print the degree of symmetry
