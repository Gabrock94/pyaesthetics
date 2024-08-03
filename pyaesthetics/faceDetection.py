#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module is used to detect (frontal) faces within an image.
It uses OpenCV's (cv2) Haar cascade for the detection or the package face-detection.
CV2 model is faster but less accurate (good for front-facing images).
Detection using the face-detection package can be done via the 'hog' or 'cnn' methods.
See the face-detection package documentation for details.

Created on Mon Apr 16 22:40:46 2018
Last edited on Fri Aug 2 10:30:14 2024

@author: Giulio Gabrieli (gack94@gmail.com).com)
"""

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import face_recognition
from PIL import Image

###############################################################################
#                                                                             #
#                      Frontal Faces Detection                                #
#                                                                             #
###############################################################################

def detectFacesCv2(img, plot=False):
    """ This function uses CV2 to detect faces in a picture.
    
        :param img: image to analyze in RGB
        :type img: numpy.ndarray
        :param plot: whether to plot or not the results
        :type plot: bool
        :return: list of detected faces as rectangles
        :rtype: list
    """
    # Convert the image to grayscale as Haar cascades work better on grayscale images
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Load the Haar cascade for frontal face detection
    frontalface_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Detect faces in the image
    faces = frontalface_cascade.detectMultiScale(img, 1.3, 5)
    
    # If plot is True, draw rectangles around detected faces and display the image
    if plot:
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            plt.imshow(img)

    # Return the list of detected faces
    return faces

def detectFaces(img, plot=False, model='hog'):
    """ This function uses face-recognition to detect faces in a picture.
        By default it uses the hog method. cnn method can be passed as model parameter.
    
        :param img: path to the image to analyze
        :type img: string
        :param plot: whether to plot or not the results
        :type plot: bool
        :param model: which model to use for the detection of faces (hog or cnn). Default is 'hog'.
        :type model: string
        :return: list of detected faces as rectangles
        :rtype: list
    """

    # Convert the image to grayscale as Haar cascades work better on grayscale images
    image = face_recognition.load_image_file(img)
    faces = face_recognition.face_locations(image, model=model)
    # If plot is True, draw rectangles around detected faces and display the image
    if plot:
        for top, right, bottom, left in faces:
            cv2.rectangle(image, (left, top), (right, bottom), (255, 0, 0), 2)
            plt.imshow(image)

    # if plot:
    #     for top, right, bottom, left in faces:
    #     # You can access the actual face itself like this:
    #         face_image = image[top:bottom, left:right]
    #         pil_image = Image.fromarray(face_image)
    #         pil_image.show()
        
    # Return the list of detected faces
    return faces

###############################################################################
#                                                                             #
#                                   DEBUG                                     #
#                                                                             #
###############################################################################

if __name__ == '__main__':
    # Get the base path of the script
    basepath = os.path.dirname(os.path.realpath(__file__))
    imagepath = "/home/giulio/Repositories/pyaesthetics/share/data/jade2.png"
    
    # Read the sample image
    img = cv2.imread(imagepath)
    
    # Convert the image to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Detect faces in the image and plot the results
    faces = detectFacesCv2(img, plot=True)
    
    # Print the number of faces detected
    # print("Number of faces in the picture is:", len(faces))

    # Detect faces in the image and plot the results
    faces = detectFaces(imagepath, plot=True)
    
    # Print the number of faces detected
    print("Number of faces in the picture is:", len(faces))

    