# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to compute the number of indipendent areas in an image.

Created on Sat Apr 21 09:40:45 2018

@author: giulio
"""

import os #to handle filesystem files
import cv2 #for image manipulation
import numpy as np
from imutils import perspective
from imutils import contours
import numpy as np
import imutils
from scipy import ndimage
import matplotlib.pyplot as plt #for data visualization
import matplotlib.patches as patches #for legends and rectangle drawing in QTD
import pytesseract
from PIL import Image
###############################################################################
#                                                                             #
#                                  Symmetry                                   #
#                                                                             #
###############################################################################
""" Thìs sections handles Quadratic Tree Decomposition. """

def textDetection(img):
    """ This function uses pytesseract to get information about the presence of text in an image
        
        :param img: image to analyze, in RGB
        :type img: numpy.ndarray
        :return: number of character in the text
        :rtype: int
    
    """
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, img)
    text = pytesseract.image_to_string(Image.open(filename))
    os.remove(filename)
    return(len(text))


def textImageRatio(areas):
    """ This function evaluates the text on image ration, as well as the total area occupied by both image and text.
    
        :param areas: areas dict as extracted by the getAreas function
        :type areas: dict
        :return: a dict containing the text / (image+text) ratio , total area of text and total area of images and number of images
        :rtype: dict
    """
    image = []
    text = []
    for area in areas:
        if(areas[area]["type"] == "Text"):
            text.append(areas[area]["area"])
        else:
            image.append(areas[area]["area"])

    """ ratio is 0.5 if picture and text occupy the same area, more in more text, less if more images. """
    ratio = sum(text) / (sum(image) + sum(text))
    return({"textImageRatio":ratio,"textArea":sum(text),"imageArea":sum(image),"nImages":len(image)})
        
def getAreas(img,minArea = 100,resize=True,newSize=[600,400],plot=False, coordinates=False, areatype=True):
    
    """ Adapted from https://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/"""
    
    img_original = img #source of the image 
    oh, ow,dept = img_original.shape #shape of the orignal image
    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) #conversion to greyscale
    if(resize):
        img = cv2.resize(img,(newSize[0],newSize[1]),interpolation=cv2.INTER_CUBIC) #resizing
    img = cv2.GaussianBlur(img, (3,3), 0)#apply a Gaussina filter
    edged = cv2.Canny(img, 10,100) 
    edged = cv2.dilate(edged, None, iterations=1)
    edged = cv2.erode(edged, None, iterations=1) #improved edge detection
    
    cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) #get the contours
    cnts = cnts[0] 

    if(len(cnts) > 0):
        (cnts, _) = contours.sort_contours(cnts) 
        
        boxes = []
        for c in cnts: #for each contour 
            box = cv2.minAreaRect(c)
            box = cv2.cv.BoxPoints(box) if imutils.is_cv2() else cv2.boxPoints(box)
            box = np.array(box, dtype="int")
            box = perspective.order_points(box)
            box = box.astype('int')
            if(resize):
                box = np.array([[int(corner[0]*ow / newSize[0]),int(corner[1]*oh / newSize[1])] for corner in box]) #convert the box to the size of the original image
            else:
                box = np.array([[int(corner[0]),int(corner[1])] for corner in box]) #convert the box to the size of the original image
            if(plot):
                cv2.drawContours(img_original, [box], -1, (0, 255, 0), 2)
            boxes.append(box)

        if(plot):
            plt.figure("Space based Decomposition")
            plt.imshow(img_original)
            plt.title("Space based decomposition")
            plt.xticks([],[])
            plt.yticks([],[])
            plt.show()
        """ Now, we can calculate the area of each box, and we can detect if some text is present"""
        areas = {}

        areasize = []
        for box in range(0,len(boxes)): #to avoid errors due to two or more rectangles of the same Area
            t = np.transpose(boxes[box])
            minX = min(t[0])
            maxX = max(t[0])
            minY = min(t[1])
            maxY = max(t[1])
            area = (maxX - minX) * (maxY - minY)
            if(area > minArea):
                areasize.append(area)
                imgportion = img_original[minY:maxY,minX:maxX]
                if(len(imgportion) > 0):
                    if(areatype):
                        if(textDetection(imgportion) > 0):
                            areas[box] = {"area":area,"type":"Text"}
                        else:
                            areas[box] = {"area":area,"type":"Image"}

                    else:
                        areas[box] = {"area":area}
                    if(coordinates):
                        areas[box]['coordinates'] = {"xmin": minX,"xmax": maxX,"ymin": minY,"ymax": maxY}

    return(areas)
            
###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################
        
""" For debug purposes."""

if(__name__=='__main__'):

    img = "/home/giulio/Repositories/PrettyWebsite/prettywebsite/sample2.jpg" #path to a sample image
    
    img = cv2.imread(img)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    areas = getAreas(img,plot=False, coordinates=True, areatype=False)

    # print(areas)
    # print(textImageRatio(areas))
    
