#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This is an entrypoint for automatic analysis of a website. 

Created on Mon Apr 16 22:40:46 2018

@author: giulio
"""

import os
import cv2
import matplotlib.pyplot as plt
import pytesseract 
from PIL import Image

###############################################################################
#                                                                             #
#                      Quadratic Tree Decomposition                           #
#                                                                             #
###############################################################################
def textDetection(img):
    """ This function uses pytesseract to get information about the presence of text in an image
        
        :param img: image to analyze, in RGB
        :type img: numpy.ndarray
        :return: number of character in the text
        :rtype: int
    
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, img)
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return(len(text))
    
def analyzeWebsite(pathToImg,resize=True, newSize=(600,400), minStd = 10, minSize = 20):
    """ This functions act as entrypoint for dummy analysis of a website aesthetic features """

    resultdict = {}
    img = cv2.imread(pathToImg)
    # plt.imshow(img)
    # plt.show()
    
    imageColor = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    imageBW = cv2.imread(pathToImg,0)
    resultdict["Text"] = textDetection(imageColor) #this has to be done before preprocessing
    imageColor_O = imageColor #keep a copy at original size
    if(resize):
        imageBW = cv2.resize(imageBW,newSize,interpolation=cv2.INTER_CUBIC)
        imageColor = cv2.resize(imageColor,newSize,interpolation=cv2.INTER_CUBIC)
    imgsRGB2RGB = brightness.sRGB2RGB(img)
    resultdict["brightness_BT709"] = brightness.relativeLuminance_BT709(imgsRGB2RGB)
    resultdict["brightness_BT601"] = brightness.relativeLuminance_BT601(imgsRGB2RGB)
    resultdict["VC_quadTree"] = len(quadTreeDecomposition.quadTree(imageBW,minStd,minSize).blocks)
    resultdict["VC_weight"] = os.stat(pathToImg).st_size
    resultdict["Symmetry_QTD"] = symmetry.getSymmetry(imageBW,minStd,minSize)
    resultdict["Colorfulness_HSV"] = colorfulness.colorfulnessHSV(imageColor)
    resultdict["Colorfulness_RGB"] = colorfulness.colorfulnessRGB(imageColor)
    resultdict["Faces"] = faceDetection.getFaces(imageColor)
    resultdict["Number_of_Faces"] = len(resultdict["Faces"])
    resultdict["Colors"] = colorDetection.getColorsW3C(imageColor)
    A = spaceBasedDecomposition.getAreas(imageColor_O)
    Adict = spaceBasedDecomposition.textImageRatio(A)
    resultdict["Number_of_Images"] = Adict["nImages"]
    resultdict["TextImageRatio"] = Adict["textImageRatio"]
    resultdict["textArea"] = Adict["textArea"]
    resultdict["imageArea"] = Adict["imageArea"]
    return(resultdict)

if(__name__=='__main__'):
    import quadTreeDecomposition
    import spaceBasedDecomposition
    import colorfulness
    import brightness
    import symmetry
    import faceDetection
    import colorDetection

    sampleImg = "/home/giulio/Repositories/PrettyWebsite/prettywebsite/sample.jpg" #path to a sample image
    results = analyzeWebsite(sampleImg)
    print(results)
else:
    from . import quadTreeDecomposition
    from . import colorfulness
    from . import brightness
    from . import symmetry
    from . import faceDetection
    from . import colorDetection
    from . import spaceBasedDecomposition