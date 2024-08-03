#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module is used to evaluate the visual complexity of an image. 

Created on Sat Aug  3 11:34:57 2024

@author: giulio
"""

import os
import cv2  # OpenCV library for image processing
import matplotlib.pyplot as plt  # Matplotlib for plotting images
from PIL import Image  # Python Imaging Library for image processing
import numpy as np

# Attempt to import internal modules of pyaesthetics, handling both relative and absolute imports
try:
    from . import quadTreeDecomposition
    from . import utils
except:
    import quadTreeDecomposition
    import utils


def getVisualComplexityQuadTree(image, minStd, minSize):
    #image must be BW
    blocks = quadTreeDecomposition.quadTree(image, minStd, minSize).blocks
    return(len(blocks))

def getVisualComplexityGradient(image):
    
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
    
    return(np.mean(merged_gradient).astype(float))
    

if __name__ == '__main__':
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    datafolder = basepath + "/../share/data/"
    
    # Path to a sample image
    sampleImg = datafolder + "panda.jpg"

    image = cv2.imread(sampleImg)
    imageBW = cv2.imread(sampleImg, 0)

    # Analyze the sample image using the 'complete' method
    qt = getVisualComplexityQuadTree(imageBW, minStd=10, minSize=20)
    grad = getVisualComplexityGradient(image)
    # Print the analysis results
    print(qt, grad)

