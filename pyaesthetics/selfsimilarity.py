#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module is used to evaluate the self-similarity and anisotropy of an image.
It is based on Braun, J., Amirshahi, S. A., Denzler, J., & Redies, C. (2013).
Statistical image properties of print advertisements, visual artworks, and images of architecture.
Frontiers in Psychology, 4, 808.

Created on Sat Aug 3 11:34:57 2024
Last edited on Sat Aug 3 14:09:43 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
from skimage.feature import hog
from skimage import exposure
from tqdm import tqdm

try:
    from . import utils
except:
    import utils

###############################################################################
#                                                                             #
#                             Self Similarity                                 #
#                                                                             #
###############################################################################

def preprocess_image(image_path):
    """
    Open an image, convert it to LAB color space, split into L, a, and b channels, 
    and calculate the gradient of each channel. Then merge the gradients by taking
    the maximum value for each pixel from the three gradients.
    
    :param image_path: Path to the input image.
    :return: Merged gradient image.
    """
    # Read the input image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Image not found at path: {image_path}")
    
    # Resize the image to a standard size
    resized_image = cv2.resize(image, (1024, 1024), interpolation=cv2.INTER_CUBIC)
    
    # Convert the image to LAB color space
    lab_image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2Lab)
    
    # Split the LAB image into L, a, and b channels
    L, a, b = cv2.split(lab_image)
    
    # Calculate the gradient for each channel
    grad_L = utils.calculate_gradient(L)
    grad_a = utils.calculate_gradient(a)
    grad_b = utils.calculate_gradient(b)
    
    # Merge the gradients by taking the maximum value for each pixel
    merged_gradient = np.maximum(np.maximum(grad_L, grad_a), grad_b)
    
    return merged_gradient

def calculate_hog(image, orientations=16, pixels_per_cell=(16, 16), cells_per_block=(2, 2), visualize=True):
    """
    Calculate the Histogram of Oriented Gradients (HOG) for a given image.
    
    :param image: Input image.
    :param orientations: Number of orientation bins.
    :param pixels_per_cell: Size (in pixels) of a cell.
    :param cells_per_block: Number of cells in each block.
    :param visualize: Whether to return an image of the HOG.
    :return: HOG feature vector and HOG image (if visualize is True).
    """
    hog_features, hog_image = hog(image, orientations=orientations, pixels_per_cell=pixels_per_cell,
                                  cells_per_block=cells_per_block, visualize=visualize, block_norm='L2-Hys')
    return hog_features, hog_image

def bin_hog_features(hog_features, n_bins):
    """
    Bin the HOG features into n bins.
    
    :param hog_features: HOG feature vector.
    :param n_bins: Number of bins.
    :return: Binned HOG feature vector.
    """
    # Calculate the size of each bin
    bin_size = len(hog_features) // n_bins
    
    # Normalize the HOG features
    hog_features = hog_features / sum(hog_features)
    
    # Sum the HOG features into n bins
    binned_hog_features = np.sum(hog_features.reshape(bin_size, n_bins), axis=0)
    
    return binned_hog_features

def plot_hog_histogram(binned_hog_features, n_bins):
    """
    Plot the histogram of the binned HOG features.
    
    :param binned_hog_features: Binned HOG feature vector.
    :param n_bins: Number of bins.
    """
    plt.figure(figsize=(10, 6))
    plt.bar(range(n_bins), binned_hog_features, align='center', alpha=0.7)
    plt.xlabel('Bin')
    plt.ylabel('Sum of Magnitudes')
    plt.title('Histogram of Oriented Gradients (HOG) with 16 Bins')
    plt.show()

def get_self_similarity(image, methods=['ground', 'parent', 'neighbors', 'anisotropy']):
    """
    Calculate the self-similarity and anisotropy of an image using HOG features.

    :param image: Input image.
    :param methods: List of methods to calculate self-similarity. Options are 'ground', 'parent', 'neighbors', 'anisotropy'.
    :return: Dictionary of self-similarity measures.
    """
    results = {}
    
    # Resize the image to a standard size
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
    
    # Calculate HOG features for the merged gradient
    hog_features, hog_image = hog(merged_gradient, orientations=16, pixels_per_cell=(16, 16),
                                  cells_per_block=(2, 2), visualize=True, block_norm='L2-Hys')
    
    hists = []
    
    print('Computing HOGs. This is going to take some time.')
    nLevels = 4  # Number of levels in the pyramid
    for level in tqdm(range(nLevels)):
        this_level = []
        
        h, w = merged_gradient.shape
        hn = h // (2**level)
        wn = w // (2**level)
        
        for i in range(0, h, hn):
            for j in range(0, w, wn):
                partial_image = merged_gradient[i:i+hn, j:j+wn]
                hog_features, hog_image = calculate_hog(partial_image, orientations=16)
                
                # Bin the HOG features into n bins
                hist = bin_hog_features(hog_features, 16)
                this_level.append(hist)
                
        hists.append(np.array(this_level))
    
    # Ground method
    if 'ground' in methods:
        ground = hists[0].flatten()
        results['ground'] = np.median([(np.sum([min(ground[n], y[n]) for n in range(16)])) for y in hists[3]]).astype(float)

    # Parent approach
    if 'parent' in methods:
        temp = []
        for i in range(len(hists[-2])):
            nodes = utils.find_child_nodes(i)
            temp.append(np.median([(np.sum([min(hists[2][i][n], y[n]) for n in range(16)])) for y in hists[3][nodes]]))
        results['parent'] = np.median(temp).astype(float)
    
    # Neighbors approach
    if 'neighbors' in methods:
        temp = []
        for i in range(len(hists[3])):
            nodes = utils.find_neighbors(i)
            temp.append(np.median([(np.sum([min(hists[3][i][n], y[n]) for n in range(16)])) for y in hists[3][nodes]]))
        results['neighbors'] = np.median(temp).astype(float)
    
    # Anisotropy
    if 'anisotropy' in methods:
        results['anisotropy'] = np.std(hists[-1]).astype(float)
    
    return results

###############################################################################
#                                                                             #
#                                  DEBUG                                      #
#                                                                             #
###############################################################################

if __name__ == "__main__":
    basepath = os.path.dirname(os.path.realpath(__file__))

    # Path to a sample image for debugging   # Set the data path to use sample images
    data_folder = basepath + "/../share/data/"
    
    # Path to a sample image
    sample_img = data_folder + "panda.jpg"
    
    # Read the sample image
    image = cv2.imread(sample_img)
    
    # Calculate self-similarity
    results = get_self_similarity(image)
    
    # Print the results
    print(results)
