#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This modules contains different utilities  that are used across different modules in pyaesthetics.

Created on Fri Aug 2 10:51:17 2024
Last Edited on Sat Aug 3 11:53:30 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

import os

from PIL import Image #to handle filesystem files
import cv2 #for image manipulation
import numpy as np #numerical computation
import pandas as pd 
import pytesseract  # Pytesseract for Optical Character Recognition (OCR)
from imutils.perspective import four_point_transform
import matplotlib.pyplot as plt 

try:
    from . import analysis
except:
    import analysis

def sRGB2RGB(img):
    """ this function converts a sRGB img to linear RGB values.
    
        It loops through each pixel, and apply a conversion to pass from sRGB to linear RGB value.
        
    
        :param img: image to analyze, in sRGB
        :type img: numpy.ndarray
        :return: image to analyze, in RGB
        :rtyipe: numpy.ndarray
    """

    img = img.flatten()
    def converter(p):
        if(p < 0.04045):
            return(p/3294.6)
        else:
            return((((p/255) + 0.055) / 1.055)**2.4)

    newimg = pd.Series(img).apply(converter).to_numpy()
    return(newimg)

def find_parent_node(i):
    """
    Find the parent node in a 4x4 matrix given an index in an 8x8 matrix.

    :param i: Index in the 8x8 matrix.
    :return: Parent node index in the 4x4 matrix.
    """
    if i < 0 or i >= 64:
        raise ValueError("Index must be in the range [0, 63]")

    # Calculate the row and column in the 8x8 matrix
    row = i // 8
    col = i % 8

    # Determine the 2x2 block's row and column in the 4x4 matrix
    block_row = row // 2
    block_col = col // 2

    # Calculate the index in the 4x4 matrix
    parent_index = block_row * 4 + block_col

    return parent_index

def find_child_nodes(parent_index):
    """
    Find the child nodes in an 8x8 matrix given a parent node index in a 4x4 matrix.

    :param parent_index: Index in the 4x4 matrix.
    :return: List of child node indices in the 8x8 matrix.
    """
    if parent_index < 0 or parent_index >= 16:
        raise ValueError("Parent index must be in the range [0, 15]")

    # Calculate the row and column in the 4x4 matrix
    parent_row = parent_index // 4
    parent_col = parent_index % 4

    # Determine the top-left corner of the 2x2 block in the 8x8 matrix
    top_left_row = parent_row * 2
    top_left_col = parent_col * 2

    # List the indices of the 4 child nodes in the 2x2 block
    child_indices = [
        top_left_row * 8 + top_left_col,       # Top-left
        top_left_row * 8 + top_left_col + 1,   # Top-right
        (top_left_row + 1) * 8 + top_left_col, # Bottom-left
        (top_left_row + 1) * 8 + top_left_col + 1 # Bottom-right
    ]

    return child_indices


def find_neighbors(index, size=8):
    """
    Find all neighboring cells for a given cell index in an NxN matrix.

    :param index: Index of the cell in the NxN matrix.
    :param size: Size of the matrix (default is 8 for an 8x8 matrix).
    :return: List of neighboring cell indices.
    """
    row = index // size
    col = index % size

    neighbors = []

    # Directions for neighbors: (row_offset, col_offset)
    directions = [
        (-1, 0),  # Top
        (1, 0),   # Bottom
        (0, -1),  # Left
        (0, 1),   # Right
        (-1, -1), # Top-left
        (-1, 1),  # Top-right
        (1, -1),  # Bottom-left
        (1, 1)    # Bottom-right
    ]

    for dr, dc in directions:
        r, c = row + dr, col + dc
        if 0 <= r < size and 0 <= c < size:
            neighbors.append(r * size + c)

    return neighbors

def calculate_gradient(image):
    """
    Calculate the gradient of an image using the Sobel operator.
    
    :param image: Input image (single channel).
    :return: Gradient magnitude of the image.
    """
    grad_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
    grad_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)
    gradient_magnitude = cv2.magnitude(grad_x, grad_y)
    
    return gradient_magnitude


def runtest():
    """ This function runs a complete test to verify the integroty
            of the installation.

        :return: a funny string
        :rtype: string

    """
    basepath = os.path.dirname(os.path.realpath(__file__))
    # Path to a sample image for debugging   # Set the data path to use sample images
    datafolder = basepath + "/../share/data/"
    # Path to a sample image
    sampleImg = datafolder + "test.png"
    # Analyze the sample image using the 'complete' method
    print('Running test')
    analysis.analyze_image(sampleImg, method='complete')
    
    return('All good! Enjoy Pyaesthetics.')

def textdetection(img):
    """ This function uses pytesseract to get information about the presence of text in an image.

        :param img: image to analyze, in RGB
        :type img: numpy.ndarray
        :return: number of characters in the text
        :rtype: int

    """
    # Convert the image to grayscale
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Save the image to a temporary file
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, img)
    # Perform OCR to extract text from the image
    text = pytesseract.image_to_string(Image.open(filename))
    # Remove the temporary file
    os.remove(filename)
    # Return the length of the extracted text
    return len(text)

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
""" For debug purposes."""

if __name__ == "__main__":
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"
    
    img = cv2.imread(sample_img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    runtest()
    