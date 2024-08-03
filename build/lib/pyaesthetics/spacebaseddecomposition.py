# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to compute the number of independent areas in an image.

Created on Sat Apr 21 09:40:45 2018
Last edited on Fri Aug 2 12:49:23 2024

@author: giulio
"""

import os  # To handle filesystem files
import cv2  # For image manipulation
import numpy as np  # For numerical operations
from imutils import perspective  # For image perspective transformations
from imutils import contours  # For contour-related utilities
import imutils  # For various image utilities
from scipy import ndimage  # For scientific image processing
import matplotlib.pyplot as plt  # For data visualization
import matplotlib.patches as patches  # For legends and rectangle drawing
import pytesseract  # For OCR
from PIL import Image  # For image processing with PIL

try:
    from . import utils
except: 
    import utils

###############################################################################
#                                                                             #
#                               Text to Image Ratio                           #
#                                                                             #
###############################################################################

def text2image_ratio(areas):
    """ This function evaluates the text-to-image ratio, as well as the total area occupied by both image and text.
    
        :param areas: areas dict as extracted by the get_areas function
        :type areas: dict
        :return: a dict containing the text / (image+text) ratio, total area of text, total area of images, and number of images
        :rtype: dict
    """
    
    image = []
    text = []
    for area in areas:
        if areas[area]["type"] == "Text":
            text.append(areas[area]["area"])
        else:
            image.append(areas[area]["area"])

    # Calculate ratio of text to the total area (text + image)
    if (sum(image) + sum(text)) > 0:
        ratio = sum(text) / (sum(image) + sum(text))
    else:
        ratio = np.nan
    return {"text2image_ratio": ratio, "textArea": sum(text), "imageArea": sum(image), "nImages": len(image)}

###############################################################################
#                                                                             #
#                                Get Areas                                    #
#                                                                             #
###############################################################################

def get_areas(img, minArea=100, resize=True, newSize=[600, 400], plot=False, coordinates=False, areatype=True, returnbox=False):
    """ Detects and returns areas in an image based on contours.
    
    :param img: Source image.
    :type img: numpy.ndarray
    :param minArea: Minimum area threshold for detected objects.
    :type minArea: int
    :param resize: Whether to resize the image.
    :type resize: bool
    :param newSize: New size for resizing the image.
    :type newSize: list
    :param plot: Whether to plot the detected areas.
    :type plot: bool
    :param coordinates: Whether to include coordinates in the result.
    :type coordinates: bool
    :param areatype: Whether to classify areas as text or image.
    :type areatype: bool
    :param returnbox: Whether to include box points in the result.
    :type returnbox: bool
    :return: Dictionary with detected areas and their properties.
    :rtype: dict
    """
    
    img_original = img  # Copy the original image
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    gray = cv2.GaussianBlur(gray, (7, 7), 0)  # Apply Gaussian blur
    # Perform edge detection, then perform dilation + erosion to close gaps in between object edges
    edged = cv2.Canny(gray, 50, 100)  # Detect edges
    edged = cv2.dilate(edged, None, iterations=1)  # Dilate edges
    edged = cv2.erode(edged, None, iterations=1)  # Erode edges to refine
    # Find contours in the edge map
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)  # Grab contours
    
    areas = {}
    
    if len(cnts) > 0:
        # Sort the contours from left-to-right
        (cnts, _) = contours.sort_contours(cnts)
        
        boxes = []
        for c in cnts:
            # Compute bounding box for each contour
            x, y, w, h = cv2.boundingRect(c)
            box = [x, y, x + w, y + h]
            
            minX, minY, maxX, maxY = box
            area = (maxX - minX) * (maxY - minY)
            if area > minArea:
                boxes.append(box)
        
        if plot:
            # Plot the detected bounding boxes
            img_plot = img_original.copy()
            for box in boxes:
                cv2.rectangle(img_plot, (box[0], box[1]), (box[2], box[3]), (0, 255, 0), 2)
            plt.figure("Space-based Decomposition")
            plt.imshow(cv2.cvtColor(img_plot, cv2.COLOR_BGR2RGB))
            plt.title("Space-based Decomposition")
            plt.xticks([])
            plt.yticks([])
            plt.show()
        
        for i, box in enumerate(boxes):
            minX, minY, maxX, maxY = box
            imgportion = img_original[minY:maxY, minX:maxX]
            area = (maxX - minX) * (maxY - minY)
            
            if len(imgportion) > 0:
                if areatype:
                    if utils.textdetection(imgportion) > 0:
                        areas[i] = {"area": area, "type": "Text"}
                    else:
                        areas[i] = {"area": area, "type": "Image"}
                else:
                    areas[i] = {"area": area}
                if coordinates:
                    areas[i]['coordinates'] = {"xmin": minX, "xmax": maxX, "ymin": minY, "ymax": maxY}
                if returnbox:
                    areas[i]['box'] = box
                        
    return areas

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes."""

import math

if(__name__=='__main__'):

    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"
    
    # Read the image with alpha channel
    img = cv2.imread(sample_img, cv2.IMREAD_UNCHANGED)
    # Convert BGRA image to RGBA
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    
    # Detect areas in the image
    areas = get_areas(img, minArea=10, plot=True, coordinates=True, areatype=True, resize=True, returnbox=True)
  