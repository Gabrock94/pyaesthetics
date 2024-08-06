#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module is used to evaluate the visual complexity of an image. 

Created on Sat Aug  3 11:34:57 2024
Last edited on Sat Aug 13:46:43 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

import os
import cv2  # OpenCV library for image processing
import matplotlib.pyplot as plt  # Matplotlib for plotting images
from PIL import Image  # Python Imaging Library for image processing
import numpy as np  # NumPy for numerical operations

# Attempt to import internal modules of pyaesthetics, handling both relative and absolute imports
try:
    from . import quadtreedecomposition
    from . import utils
except:
    import quadtreedecomposition
    import utils


###############################################################################
#                                                                             #
#                            Visual Complexity                                #
#                                                                             #
###############################################################################

def get_visual_complexity_quadtree(image, minStd, minSize, standardized=True, autoadjust=False):
    """
    Calculate the visual complexity of an image using quadtree decomposition.
    It can return the standardized (default) visual complexity, with 1 being the 
    highest complexity possible, or unstandardized (which is the number of leaves
    resulting from the quadratic tree decomposition).

    :param image: Input image (grayscale).
    :type image: numpy.ndarray
    :param minStd: Minimum standard deviation for splitting blocks.
    :type minStd: int
    :param minSize: Minimum size of blocks.
    :type minSize: int
    :param standardized: Whether to return standardized complexity.
    :type standardized: bool
    :param autoadjust: Whether to automatically adjust the minSize parameter.
    :type autoadjust: bool
    :return: Standardized complexity if `standardized` is True, otherwise the number of blocks.
    :rtype: float or int
    """
    # Perform quadtree decomposition
    quadtree = quadtreedecomposition.quadTree(image, minStd, minSize, autoadjust)
    
    if(standardized):
        return(quadtree.standardized_complexity)
    else:
        # Return the number of blocks
        return(quadtree.nblocks)

def get_visual_complexity_gradient(image):
    """
    Calculate the visual complexity of an image using gradient magnitude.

    :param image: Input image (color).
    :return: Mean of the merged gradient magnitudes.
    """
    # Resize the image to 1024x1024
    image = cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_CUBIC)
    
    # Convert the image to LAB color space
    lab_image = cv2.cvtColor(image, cv2.COLOR_BGR2Lab)
    
    # Split the LAB image into L, a, and b channels
    L, a, b = cv2.split(lab_image)
    
    # Calculate the gradient for each channel
    grad_L = utils.calculate_gradient(L)
    grad_a = utils.calculate_gradient(a)
    grad_b = utils.calculate_gradient(b)
    
    # Merge the gradients by taking the maximum value for each pixel
    merged_gradient = np.maximum(np.maximum(grad_L, grad_a), grad_b)
    
    # Return the mean of the merged gradient magnitudes
    return(np.mean(merged_gradient).astype(float))
    
def get_visual_complexity_weight(path_to_image):
    """
    Calculate the visual complexity of an image based on its file size.

    :param path_to_image: Path to the image file.
    :return: File size in bytes.
    """
    # Return the file size in bytes
    return(os.stat(path_to_image).st_size)

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################

if __name__ == '__main__':
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Set the data path to use sample images
    datafolder = os.path.join(basepath, "../share/data/")
    
    # Path to a sample image
    sample_img_path = os.path.join(datafolder, "panda.jpg")

    # Read the sample image in color and grayscale
    image = cv2.imread(sample_img_path)
    image_bw = cv2.imread(sample_img_path, 0)

    # Analyze the sample image using quadtree decomposition and gradient magnitude methods
    qt_complexity = get_visual_complexity_quadtree(image_bw, minStd=10, minSize=20)
    grad_complexity = get_visual_complexity_gradient(image)
    
    # Print the analysis results
    print(qt_complexity, grad_complexity)
