#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to evaluate the presence of different colors in an image.
It uses the 16 basic colors or the full 140 color list defined in the W3C specifications.

Created on Thu Apr 19 22:40:46 2018
Last edited on Fri Aug 2 11:37:57 2024

@author: Giulio Gabrieli (gack94@gmail.com)
"""

import os
import cv2
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches
import time
import pandas as pd
###############################################################################
#                                                                             #
#                  This section handles color recognition                     #
#                                                                             #
###############################################################################

# Define color dictionaries for 16 and 140 W3C colors
_colors = {
    16: {
        "Aqua": [0, 255, 255],
        "Black": [0, 0, 0],
        "Blue": [0, 0, 255],
        "Fuchsia": [255, 0, 255],
        "Gray": [128, 128, 128],
        "Green": [0, 128, 0],
        "Lime": [0, 255, 0],
        "Maroon": [128, 0, 0],
        "Navy": [0, 0, 128],
        "Olive": [128, 128, 0],
        "Purple": [128, 0, 128],
        "Red": [255, 0, 0],
        "Silver": [192, 192, 192],
        "Teal": [0, 128, 128],
        "White": [255, 255, 255],
        "Yellow": [255, 255, 0]
    },
    140: {
        "AliceBlue" : [240,248,255],
        "AntiqueWhite" : [250,235,215],
        "Aqua" : [0,255,255],
        "AquaMarine" : [127,255,212],
        "Azure" : [240,255,255],
        "Beige" : [245,245,220],
        "Bisque" : [255,228,196],
        "Black" : [0,0,0],
        "BlanchedAlmond" : [255,235,205],
        "Blue" : [0,0,255],
        "BlueViolet" : [138,43,226],
        "Brown" : [165,42,42],
        "BurlyWood" : [222,184,135],
        "CadetBlue" : [95,158,160],
        "Chartreuse" : [127,255,0],
        "Chocolate" : [210,105,30],
        "Coral" : [255,127,80],
        "CornFlowerBlue" : [100,149,237],
        "Cornsilk" : [255,248,220],
        "Crimson" : [220,20,60],
        "Cyan" : [0,255,255],
        "DarkBlue" : [0,0,139],
        "DarkCyan" : [0,139,139],
        "DarkGoldenRod" : [184,134,11],
        "DarkGray" : [169,169,169],
        "DarkGreen" : [0,100,0],
        "DarkKhaki" : [189,183,107],
        "DarkMagenta" : [139,0,139],
        "DarkOliveGreen" : [85,107,47],
        "DarkOrange" : [255,140,0],
        "DarkOrchid" : [153,50,204],
        "DarkRed" : [139,0,0],
        "DarkSalmon" : [233,150,122],
        "DarkSeaGreen" : [143,188,143],
        "DarkSlateBlue" : [72,61,139],
        "DarkSlateGray" : [47,79,79],
        "DarkTurquoise" : [0,206,209],
        "DarkViolet" : [148,0,211],
        "DeepPink" : [255,20,147],
        "DeepSkyBlue" : [0,191,255],
        "DimGray" : [105,105,105],
        "DodgerBlue" : [30,144,255],
        "FireBrick" : [178,34,34],
        "FloralWhite" : [255,250,240],
        "ForestGreen" : [34,139,34],
        "Fuchsia" : [255, 0, 255], 
        "Gainsboro" : [220,220,220],
        "GhostWhite" : [248,248,255],
        "Gold" : [255,215,0],
        "GoldenRod" : [218,165,32],
        "Gray" : [128,128,128],
        "Green" : [0,128,0],
        "GreenYellow" : [173,255,47],
        "HoneyDew" : [240,255,240],
        "HotPink" : [255,105,180],
        "IndianRed" : [205,92,92],
        "Indigo" : [75,0,130],
        "Ivory" : [255,255,240],
        "Khaki" : [240,230,140],
        "Lavender" : [230,230,250],
        "LavenderBlush" : [255,240,245],
        "LawnGreen" : [124,252,0],
        "LemonChiffon" : [255,250,205],
        "LightBlue" : [173,216,230],
        "LightCoral" : [240,128,128],
        "LightCyan" : [224,255,255],
        "LightGoldenrodYellow" : [250,250,210],
        "LightGray" : [211,211,211],
        "LightGreen" : [144,238,144],
        "LightPink" : [255,182,193],
        "LightSalmon" : [255,160,122],
        "LightSeaGreen" : [32,178,170],
        "LightSkyBlue" : [135,206,250],
        "LightSlateGray" : [119,136,153],
        "LightSteelBlue" : [176,196,222],
        "LightYellow" : [255,255,224],
        "Lime" : [0,255,0],
        "LimeGreen" : [50,205,50],
        "Linen" : [250,240,230],
        "Magenta" : [255,0,255],
        "Maroon" : [128,0,0],
        "MediumAquaMarine" : [102,205,170],
        "MediumBlue" : [0,0,205],
        "MediumOrchid" : [186,85,211],
        "MediumPurple" : [147,112,219],
        "MediumSeaGreen" : [60,179,113],
        "MediumSlateBlue" : [123,104,238],
        "MediumSpringGreen" : [0,250,154],
        "MediumTurquoise" : [72,209,204],
        "MediumVioletRed" : [199,21,133],
        "MidnightBlue" : [25,25,112],
        "MintCream" : [245,255,250],
        "MistyRose" : [255,228,225],
        "Moccasin" : [255,228,181],
        "NavajoWhite" : [255,222,173],
        "Navy" : [0,0,128],
        "OldLace" : [253,245,230],
        "Olive" : [128,128,0],
        "OliveDrab" : [107,142,35],
        "Orange" : [255,165,0],
        "OrangeRed" : [255,69,0],
        "Orchid" : [218,112,214],
        "PaleGoldenRod" : [238,232,170],
        "PaleGreen" : [152,251,152],
        "PaleTurquoise" : [175,238,238],
        "PaleVioletRed" : [219,112,147],
        "PapayaWhip" : [255,239,213],
        "PeachPuff" : [255,218,185],
        "Peru" : [205,133,63],
        "Pink" : [255,192,203],
        "Plum" : [221,160,221],
        "PowderBlue" : [176,224,230],
        "Purple" : [128,0,128],
        "Red" : [255,0,0],
        "RosyBrown" : [188,143,143],
        "RoyalBlue" : [65,105,225],
        "SaddleBrown" : [139,69,19],
        "Salmon" : [250,128,114],
        "SandyBrown" : [244,164,96],
        "SeaGreen" : [46,139,87],
        "SeaShell" : [255,245,238],
        "Sienna" : [160,82,45],
        "Silver" : [192,192,192],
        "SkyBlue" : [135,206,235],
        "SlateBlue" : [106,90,205],
        "SlateGray" : [112,128,144],
        "Snow" : [255,250,250],
        "SpringGreen" : [0,255,127],
        "SteelBlue" : [70,130,180],
        "Tan" : [210,180,140],
        "Teal" : [0,128,128],
        "Thistle" : [216,191,216],
        "Tomato" : [255,99,71],
        "Turquoise" : [64,224,208],
        "Violet" : [238,130,238],
        "Wheat" : [245,222,179],
        "White" : [255,255,255],
        "WhiteSmoke" : [245,245,245],
        "Yellow" : [255,255,0],
        "YellowGreen" : [154,205,50]
        }
    }

def get_colors_w3c(img, ncolors=16, plot=False, plotncolors=5):
    """
    This function is used to get a simplified color palette (W3C colors).
    It can be used with 16 (https://www.html-color-names.com/basic-color-names.php) 
    or 140 colors (https://www.w3schools.com/colors/colors_names.asp).
    
    :param img: Image to analyze in RGB format.
    :type img: numpy.ndarray
    :param ncolors: Number of colors to use (e.g., 16 or 140). Default is 16.
    :type ncolors: int
    :param plot: Whether to plot a color palette image showing the top colors.
    :type plot: bool
    :param plotncolors: Number of colors to display in the palette image. Default is 5.
    :type plotncolors: int
    :param clusterfactor: Factor to cluster similar colors. Default is 50.
    :type clusterfactor: int
    :return: An array of RGB values representing the most frequent colors.
    :rtype: numpy.ndarray
    """
    
    # Validate ncolors
    if ncolors not in [16, 140]:
        raise ValueError("Invalid value for 'ncolors'. Value must be 16 or 140.")
    
    # Select color dictionary
    colors = _colors[ncolors]
                 
    # Calculate the distance of each pixel to each color
    colors_array = np.array(list(colors.values()))
    dists = np.sum(np.abs(img[:, :, np.newaxis, :3] - colors_array), axis=3)
    closest_color_indices = np.argmin(dists, axis=2)
    
    colorscheme = []

    # Map the indices to color names
    for row_indices in closest_color_indices:
        row_colors = [list(colors.keys())[index] for index in row_indices]
        colorscheme.extend(row_colors)
    
    # Handle alpha channel
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        # Exclude completely transparent pixels (alpha == 0) from distance calculation
        mask = alpha > 100 
        mask = mask.ravel()
        colorscheme = np.array(colorscheme)[mask]
        
    # Calculate the percentage of each color
    unique_colors, counts = np.unique(colorscheme, return_counts=True)
    colorscheme = sorted([[c, count / len(colorscheme) * 100] for c, count in zip(unique_colors, counts)])
    
    # Add missing colors with 0% presence
    missingcolors = list(set(colors) - set(unique_colors))
    for color in missingcolors:
        colorscheme.append([color, 0.0])
    
    colorscheme = sorted(colorscheme)
    
    # Plot the color palette if required
    if plot:
        sorted_data = sorted(colorscheme, key=lambda x: x[1], reverse=True)
        fig, ax = plt.subplots()
        plt.suptitle(f'Top {plotncolors} colors ({ncolors} colors mode)')
        for i in range(plotncolors):
            ax.add_patch(patches.Rectangle((i, 0), 1, 1, facecolor=sorted_data[i][0].lower()))
        plt.xlim(0, plotncolors)
        plt.axis('off')  # H
        plt.show()
    
    return colorscheme

def get_colors(img, plot=False, plotncolors=5, clusterfactor = 50):
    """
    Extracts and optionally plots the most frequent colors in an image.

    This function reshapes the image to a list of RGB values, clusters these colors 
    based on the specified cluster factor to reduce the number of unique colors, and 
    returns the most common colors. Optionally, it can plot the top `plotncolors` colors 
    as rectangles.

    Parameters:
    - img (numpy.ndarray): The input image as a NumPy array of shape (height, width, 3).
    - plot (bool): If True, a plot of the top `plotncolors` colors is displayed. Default is False.
    - plotncolors (int): The number of top colors to plot. Default is 5.
    - clusterfactor (int): The factor by which to cluster similar colors. Default is 50.

    Returns:
    - numpy.ndarray: An array of RGB values representing the most frequent colors.
    """
    
    # Reshape the image array to a list of RGB values
    data = img[:, :, :3].reshape(img.shape[0] * img.shape[1], 3)
    
    # Handle alpha channel
    if img.shape[2] == 4:
        alpha = img[:, :, 3]
        # Exclude completely transparent pixels (alpha == 0) from distance calculation
        mask = alpha > 100 
        mask = mask.ravel()
        data = np.array(data)[mask]
        
    # Apply clustering by rounding the RGB values based on clusterfactor
    data = data // clusterfactor
    data = data.astype(int)
    data = data * clusterfactor
    
    # Convert to DataFrame to use value_counts for finding the most frequent colors
    df = pd.DataFrame(data, columns=['R', 'G', 'B'])
    sorted_data = df.value_counts().index.to_numpy()
    
    if plot:
        # Plot the top `plotncolors` colors
        fig, ax = plt.subplots()
        plt.suptitle(f'Top {plotncolors} colors')
        for i in range(min(plotncolors, len(sorted_data))):
            ax.add_patch(patches.Rectangle((i, 0), 1, 1, facecolor=[x/255 for x in sorted_data[i]]))
        plt.xlim(0, plotncolors)
        plt.axis('off')  # Hide axes
        plt.show()
    
    return sorted_data

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
    sample_img = "/home/giulio/Repositories/pyaesthetics/docs/examples/pyaesthetics_small.png"

    
    # Read and preprocess the sample image
    img = cv2.imread(sample_img, cv2.IMREAD_UNCHANGED)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGBA)
    
    # Display the image
    plt.imshow(img)
    
    
    # Calculate and print the color scheme using 16 W3C colors and plot the results
    results = get_colors_w3c(img, ncolors=16, plot=True, plotncolors=5)
    print("Color scheme of the image is:", results)

    # Calculate and print the color scheme using 16 W3C colors and plot the results
    results = get_colors_w3c(img, ncolors=140, plot=True, plotncolors=5)
    print("Color scheme of the image is:", results)

    # Calculate and print the color scheme using RGB colors (reduced to cluster similar colors) and plot the results
    results = get_colors(img, plot=True, plotncolors=5, clusterfactor = 10)
    print("Color scheme of the image is:", results)