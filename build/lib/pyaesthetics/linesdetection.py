#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to evaluate the amount of straight and curved lines in an image.
This is a very experimental feature; usage is not recommended.

Created on Wed Jul 31 11:49:45 2024
Last edited on Fri Aug  2 11:46:24 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

###############################################################################
#                                                                             #
#                                   Libraries                                 #
#                                                                             #
###############################################################################

import os # to handle filesystem files
import cv2 # for image manipulation
import numpy as np # numerical computation
import pandas as pd # for data manipulation (not used in this script, but imported)
import math # for mathematical operations (not used in this script)
import matplotlib.pyplot as plt # for plotting images and results

###############################################################################
#                                                                             #
#                              Lines Detection                                #
#                                                                             #
###############################################################################

""" This section handles the detection of lines in images. """

def get_straight_lines(image, plot=False):
    """
    Detect straight lines in an image using the Hough Line Transform.

    :param image: The image to analyze, in RGB format.
    :type image: numpy.ndarray
    :param plot: Whether to plot the image with detected lines or not (default is False).
    :type plot: bool, optional
    :return: Detected straight lines.
    :rtype: list of numpy.ndarray or None
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply edge detection
    edges = cv2.Canny(gray, 25, 100, apertureSize=3)

    # Detect lines using the Hough Line Transform
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, threshold=100, minLineLength=15, maxLineGap=10)
    
    if plot:
        # Draw the lines on the image
        if lines is not None:
            for line in lines:
                x1, y1, x2, y2 = line[0]
                cv2.line(image, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Display the result with detected lines
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title('Detected Straight Lines')
        plt.show()

    return lines

def get_curved_lines(image, plot=False):
    """
    Detect curved lines (contours) in an image.

    :param image: The image to analyze, in RGB format.
    :type image: numpy.ndarray
    :param plot: Whether to plot the image with detected contours or not (default is False).
    :type plot: bool, optional
    :return: Detected contours.
    :rtype: list of numpy.ndarray
    """
    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply edge detection
    edges = cv2.Canny(gray, 50, 150)

    # Find contours in the image
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if plot:
        # Draw contours on the image
        cv2.drawContours(image, contours, -1, (255, 0, 0), 2)

        # Display the result with detected contours
        plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        plt.title('Detected Contours')
        plt.show()
        
    return contours

def calculate_distance(x1, y1, x2, y2):
    """
    Calculate the distance between two points (x1, y1) and (x2, y2).

    :param x1: The x-coordinate of the first point.
    :type x1: float
    :param y1: The y-coordinate of the first point.
    :type y1: float
    :param x2: The x-coordinate of the second point.
    :type x2: float
    :param y2: The y-coordinate of the second point.
    :type y2: float
    :return: The distance between the two points.
    :rtype: float
    """
    return np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def get_lines_ratio(lines, curves):
    """
    Calculate the ratio of the total length of straight lines to the total length of curved lines in an image.

    :param lines: List of detected straight lines.
    :type lines: list of numpy.ndarray or None
    :param curves: List of detected contours.
    :type curves: list of numpy.ndarray
    :return: The ratio of total straight line length to total curved line length. Returns NaN if division by zero occurs.
    :rtype: float
    """
    # Initialize total length
    lines_total_length = 0
    curved_total_length = 0
    
    # Calculate the total length of straight lines
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            length = calculate_distance(x1, y1, x2, y2)
            lines_total_length += length

    # Calculate the total length of curved lines (contours)
    for contour in curves:
        length = cv2.arcLength(contour, True)  # True indicates the contour is closed
        curved_total_length += length
         
    # Return the ratio of straight line length to curved line length, or NaN if division by zero occurs
    try:
        return lines_total_length / curved_total_length
    except ZeroDivisionError:
        return np.nan

def analyse_lines(image):
    """
    Analyze an image to determine the ratio of the total length of straight lines to the total length of curved lines.

    :param image: The image to analyze, in RGB format.
    :type image: numpy.ndarray
    :return: The ratio of total straight line length to total curved line length. Returns NaN if division by zero occurs.
    :rtype: float
    """
    lines = get_straight_lines(image)
    curves = get_curved_lines(image)
    ratio = get_lines_ratio(lines, curves)
    return ratio

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes, this section reads a sample image and calculates the ratio of straight to curved lines. """

if __name__ == '__main__':
    # Path to the sample image
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"

    img = cv2.imread(sample_img)
    
    # Detect straight lines and curved lines (contours)
    lines = get_straight_lines(img)
    curves = get_curved_lines(img)
    
    # Calculate and print the ratio of straight to curved lines
    ratio = get_lines_ratio(lines, curves)
    print(ratio)
