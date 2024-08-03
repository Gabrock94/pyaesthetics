#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an entrypoint for the automatic analysis of images using pyaesthetics.


Created on Mon Apr 16 22:40:46 2018
Last edited on Fri Aug 2 09:53:57 2024

@author: Giulio Gabrieli (gack94@gmail.com)
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
    from . import brightness
    from . import colordetection
    from . import colorfulness
    from . import contrast
    from . import facedetection
    from . import linesdetection
    from . import quadtreedecomposition
    from . import saturation
    from . import selfsimilarity
    from . import spacebaseddecomposition
    from . import symmetry
    from . import utils
    from . import visualcomplexity
except:
    import analysis
    import brightness
    import colordetection
    import colorfulness
    import contrast
    import facedetection
    import linesdetection
    import quadtreedecomposition
    import saturation
    import selfsimilarity
    import spacebaseddecomposition
    import symmetry
    import utils
    import visualcomplexity

###############################################################################
#                                                                             #
#                      Quadratic Tree Decomposition                           #
#                                                                             #
###############################################################################

def analyze_image(pathToImg, method='fast', resize=True, newSize=(600, 400), minStd=10, minSize=20):
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
    resultdict["Text"] = utils.textdetection(imageColor)
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
        resultdict["VC_quadTree"] = visualcomplexity.get_visual_complexity_quadtree(imageBW, minStd, minSize)
        resultdict["Symmetry_QTD"] = symmetry.get_symmetry(imageBW, minStd, minSize)
        resultdict["Colorfulness_RGB"] = colorfulness.colorfulness_rgb(imageColor)
        resultdict["contrast_RMS"] = contrast.contrast_RMS(imageColor)
        resultdict["saturation"] = saturation.saturation(imageColor)
        resultdict["linesRatio"] = linesdetection.analyse_lines(imageColor)

    elif method == 'complete':
        # Complete method: more detailed and extensive calculations
        resultdict["brightness_BT709"] = brightness.relativeluminance_bt709(imgsRGB2RGB)
        resultdict["brightness_BT601"] = brightness.relativeluminance_bt601(imgsRGB2RGB)
        resultdict["VC_quadTree"] = visualcomplexity.get_visual_complexity_quadtree(imageBW, minStd, minSize)
        resultdict["VC_gradient"] = visualcomplexity.get_visual_complexity_gradient(imageColor)
        resultdict["VC_weight"] = visualcomplexity.get_visual_complexity_weight(pathToImg)
        resultdict["Symmetry_QTD"] = symmetry.get_symmetry(imageBW, minStd, minSize)
        resultdict["Colorfulness_HSV"] = colorfulness.colorfulness_hsv(imageColor)
        resultdict["Colorfulness_RGB"] = colorfulness.colorfulness_rgb(imageColor)
        resultdict["FacesCv2"] = facedetection.detect_faces_cv2(imageColor)
        resultdict["FacesFd"] = facedetection.detect_faces(pathToImg)
        resultdict["Number_of_Faces_Cv2"] = len(resultdict["FacesCv2"])
        resultdict["Number_of_Faces_fd"] = len(resultdict["FacesFd"])
        resultdict["Colors"] = colordetection.get_colors_w3c(imageColor, ncolors=140)
        A = spacebaseddecomposition.get_areas(imageColor_O)
        Adict = spacebaseddecomposition.text2image_ratio(A)
        resultdict["Number_of_Images"] = Adict["nImages"]
        resultdict["text2image_ratio"] = Adict["text2image_ratio"]
        resultdict["textArea"] = Adict["textArea"]
        resultdict["imageArea"] = Adict["imageArea"]
        resultdict["contrast_rms"] = contrast.contrast_rms(imageColor)
        resultdict["contrast_michelson"] = contrast.contrast_michelson(imageColor)
        resultdict["saturation"] = saturation.saturation(imageColor)
        resultdict["linesRatio"] = linesdetection.analyse_lines(imageColor)
        resultdict['selfSimilarity'] = selfsimilarity.get_self_similarity(img)

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
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"
    
    # Analyze the sample image using the 'complete' method
    results = analyze_image(sample_img, method='complete')
    # Print the analysis results
    print(results)

