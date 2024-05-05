#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to compute the degree of selfsimilarity of an image.
- Self Similarity is evaluated using the PHOG method proposed in Amirshahi, S. A., Koch, M., Denzler, J., & Redies, C. (2012, February). PHOG analysis of self-similarity in aesthetic images. In Human Vision and Electronic Imaging XVII (Vol. 8291, p. 82911J). International Society for Optics and Photonics.

Created on Mon Oct 18 17:22:45 2021

@author: giulio
"""

import cv2
import numpy as np
from skimage.feature import hog

###############################################################################
#                                                                             #
#                               Self Similarity                               #
#                                                                             #
###############################################################################


class SelfSimilarity:
    """This function returns the degree of self similarity (0-1) of an image

    :param img: img to analyze
    :type img: numpy.ndarray
    :maxlevel: Maximum number of level to analyze.
    :type minStd: int
    :return: degree of self similarity
    :rtype: float
    """

    def __init__(self, img, max_level=4):
        self.image_LAB = cv2.cvtColor(
            img, cv2.COLOR_BGR2LAB
        )  # convert image to LAB Colorspace
        self.maxlevel = max_level
        hogs = self.get_hogs(self.image_LAB)

        self.get_similarity(self.image_LAB, hogs, hogs, 1)

    def get_hogs(self, img):
        h, w, _ = img.shape

        print(img.shape, "\n")

        Il, Ia, Ib = cv2.split(img)
        gIl, gIa, gIb = (
            np.gradient(Il, edge_order=2, axis=0),
            np.gradient(Ia, edge_order=2, axis=0),
            np.gradient(Ib, edge_order=2, axis=0),
        )
        gIl = np.array(gIl).flatten()
        gIa = np.array(gIa).flatten()
        gIb = np.array(gIb).flatten()
        G = np.amax(np.transpose([gIl, gIa, gIb]), 1)
        G = np.reshape(G, (h, w))
        hogs = hog(G, orientations=16)
        hogs = (hogs + min(hogs)) / sum(
            hogs + min(hogs)
        )  # normalize so that sum is 1, this is ground
        return hogs

    def get_similarity(self, img, groundhogs, parenthogs, level):
        # divide the image in four
        h, w, _ = img.shape
        w2 = int(w / 2)
        h2 = int(h / 2)
        img1, img2, img3, img4 = (
            img[:, 0:h2, 0:w2],
            img[:, 0:h2, w2:w],
            img[:, h2:h, 0:w2],
            img[:, h2:h, w2:w],
        )

        hogs1, hogs2, hogs3, hogs4 = (
            self.get_hogs(img1),
            self.get_hogs(img2),
            self.get_hogs(img3),
            self.get_hogs(img4),
        )

        print(sum(np.amin(np.transpose([hogs1, parenthogs]), 1)))
        print(sum(np.amin(np.transpose([hogs2, parenthogs]), 1)))
        print(sum(np.amin(np.transpose([hogs3, parenthogs]), 1)))
        print(sum(np.amin(np.transpose([hogs4, parenthogs]), 1)))

        if level <= self.maxlevel:
            pass


# ###############################################################################
# #                                                                             #
# #                                  DEBUG                                      #
# #                                                                             #
# ###############################################################################

# """ For debug purposes."""

# if __name__ == "__main__":
#     img = "/home/giulio/Repositories/pyaesthetics/pyaesthetics/sample2.jpg"  # path to a sample image
#     img = cv2.imread(img)  # read the image in color for plotting purposes
#     SelfSimilarity(img)
