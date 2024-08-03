#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an entrypoint for the automatic analysis of images using pyaesthetics.


Created on Mon Apr 16 22:40:46 2018
Last edited on Fri Aug 2 09:53:57 2024

@author: Giulio Gabrieli (gack94@gmail.com).com)
"""

###############################################################################
#                                                                             #
#                                 Libraries                                   #
#                                                                             #
###############################################################################

import os
import cv2  # OpenCV library for image processing
import matplotlib.pyplot as plt  # Matplotlib for plotting images
import pytesseract  # Pytesseract for Optical Character Recognition (OCR)
from PIL import Image  # Python Imaging Library for image processing

# Attempt to import internal modules of pyaesthetics, handling both relative and absolute imports
try:
    from . import quadTreeDecomposition
    from . import colorfulness
    from . import brightness
    from . import symmetry
    from . import faceDetection
    from . import colorDetection
    from . import spaceBasedDecomposition
    from . import contrast
    from . import saturation
    from . import linesDetection
    from . import utils
except:
    import quadTreeDecomposition
    import spaceBasedDecomposition
    import colorfulness
    import brightness
    import symmetry
    import faceDetection
    import colorDetection
    import contrast
    import saturation
    import linesDetection
    import utils

###############################################################################
#                                                                             #
#                      Quadratic Tree Decomposition                           #
#                                                                             #
###############################################################################

def textDetection(img):
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
    

def analyzeImage(pathToImg, method='fast', resize=True, newSize=(600, 400), minStd=10, minSize=20):
    """ This function acts as an entry point for the automatic analysis of an image's aesthetic features.
        There are two methods available: 'fast' (default) and 'complete'.
    
        The 'fast' method performs the following analysis: 
        - brightness (BT709)
        - Visual Complexity (using quadtree decomposition)
        - Symmetry (using quadtree decomposition)
        - Colorfulness (in the RGB color scheme)
        - contrast (Root Mean Square (RMS) method)
        - saturation
        - ratio between straight and curved lines

        The 'complete' method performs the following analysis:
        - brightness (BT709 and BT601)
        - Visual Complexity (using quadtree decomposition)
        - Visual Complexity (using the weight method)
        - Symmetry (using quadtree decomposition)
        - Colorfulness (in HSV and RGB color schemes)
        - Face detection and number of faces
        - Color detection
        - Number of images within an image
        - Text to image ratio
        - Surface area occupied by text and images
        - contrast (Root Mean Square (RMS) and Michelson methods)
        - saturation
        - ratio between straight and curved lines

        :param pathToImg: path to the image to analyze
        :type pathToImg: str
        :param method: set the analysis method to use. Valid methods are 'fast' and 'complete'. Default is 'fast'.
        :type method: str
        :param resize: indicate whether to resize the image (reduces computational workload, this reducing processing time)
        :type resize: bool
        :param newSize: if the image has to be resized, this tuple indicates the new size of the image
        :type newSize: tuple
        :param minStd: minimum standard deviation for the quadtree decomposition
        :type minStd: int
        :param minSize: minimum size for the quadtree decomposition
        :type minSize: int
        :return: dictionary containing the analysis results
        :rtype: dict
    """

    resultdict = {}
    # Read the image from the provided path
    img = cv2.imread(pathToImg)
    
    # Convert the image to RGB format
    imageColor = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # Read the image in grayscale
    imageBW = cv2.imread(pathToImg, 0)
    # Detect text in the image and store the result in the dictionary
    resultdict["Text"] = textDetection(imageColor)
    # Keep a copy of the original size image
    imageColor_O = imageColor
    # Resize the image if requested
    if resize:
        imageBW = cv2.resize(imageBW, newSize, interpolation=cv2.INTER_CUBIC)
        imageColor = cv2.resize(imageColor, newSize, interpolation=cv2.INTER_CUBIC)
    
    # Convert sRGB to RGB using the brightness module
    imgsRGB2RGB = utils.sRGB2RGB(img)

    # Perform analysis based on the selected method
    if method == 'fast':
        # Fast method: fewer and quicker calculations
        resultdict["brightness_BT709"] = brightness.relativeLuminance_BT709(imgsRGB2RGB)
        resultdict["VC_quadTree"] = len(quadTreeDecomposition.quadTree(imageBW, minStd, minSize).blocks)
        resultdict["Symmetry_QTD"] = symmetry.getSymmetry(imageBW, minStd, minSize)
        resultdict["Colorfulness_RGB"] = colorfulness.colorfulnessRGB(imageColor)
        resultdict["contrast_RMS"] = contrast.contrast_RMS(imageColor)
        resultdict["saturation"] = saturation.saturation(imageColor)
        resultdict["linesRatio"] = linesDetection.analyseLines(imageColor)

    elif method == 'complete':
        # Complete method: more detailed and extensive calculations
        resultdict["brightness_BT709"] = brightness.relativeLuminance_BT709(imgsRGB2RGB)
        resultdict["brightness_BT601"] = brightness.relativeLuminance_BT601(imgsRGB2RGB)
        resultdict["VC_quadTree"] = len(quadTreeDecomposition.quadTree(imageBW, minStd, minSize).blocks)
        resultdict["VC_weight"] = os.stat(pathToImg).st_size
        resultdict["Symmetry_QTD"] = symmetry.getSymmetry(imageBW, minStd, minSize)
        resultdict["Colorfulness_HSV"] = colorfulness.colorfulnessHSV(imageColor)
        resultdict["Colorfulness_RGB"] = colorfulness.colorfulnessRGB(imageColor)
        resultdict["Faces"] = faceDetection.detectFaces(imageColor)
        resultdict["Number_of_Faces"] = len(resultdict["Faces"])
        resultdict["Colors"] = colorDetection.getColorsW3C(imageColor, ncolors=140)
        A = spaceBasedDecomposition.getAreas(imageColor_O)
        Adict = spaceBasedDecomposition.textImageRatio(A)
        resultdict["Number_of_Images"] = Adict["nImages"]
        resultdict["TextImageRatio"] = Adict["textImageRatio"]
        resultdict["textArea"] = Adict["textArea"]
        resultdict["imageArea"] = Adict["imageArea"]
        resultdict["contrast_RMS"] = contrast.contrast_RMS(imageColor)
        resultdict["contrast_Michelson"] = contrast.contrast_Michelson(imageColor)
        resultdict["saturation"] = saturation.saturation(imageColor)
        resultdict["linesRatio"] = linesDetection.analyseLines(imageColor)

    # Return the result dictionary
    return resultdict


###############################################################################
#                                                                             #
#                                   DEBUG                                     #
#                                                                             #
###############################################################################


if __name__ == '__main__':
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    datafolder = basepath + "/../share/data/"
    
    # Path to a sample image
    sampleImg = datafolder + "panda.jpg"
    
    # Analyze the sample image using the 'complete' method
    results = analyzeImage(sampleImg, method='complete')
    # Print the analysis results
    print(results)

