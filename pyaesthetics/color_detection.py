#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains function to evaluate the presence of different colors of an image.
It uses the 16 basic colors defined in the W3C specifications.

@author: Giulio Gabrieli
"""

import io
from dataclasses import dataclass
from typing import Dict, Final, List, Literal, Optional, Tuple

import numpy as np
from PIL import Image
from PIL.Image import Image as PilImage

###############################################################################
#                                                                             #
#                  This section handles color recogntion                      #
#                                                                             #
###############################################################################

NColorType = Literal[16, 140]

COLORS: Final[Dict[int, Dict[str, Tuple[int, int, int]]]] = {
    16: {
        "Aqua": (0, 255, 255),
        "Black": (0, 0, 0),
        "Blue": (0, 0, 255),
        "Fuchsia": (255, 0, 255),
        "Gray": (128, 128, 128),
        "Green": (0, 128, 0),
        "Lime": (0, 255, 0),
        "Maroon": (128, 0, 0),
        "Navy": (0, 0, 128),
        "Olive": (128, 128, 0),
        "Purple": (128, 0, 128),
        "Red": (255, 0, 0),
        "Silver": (192, 192, 192),
        "Teal": (0, 128, 128),
        "White": (255, 255, 255),
        "Yellow": (255, 255, 0),
    },
    140: {
        "AliceBlue": (240, 248, 255),
        "AntiqueWhite": (250, 235, 215),
        "Aqua": (0, 255, 255),
        "AquaMarine": (127, 255, 212),
        "Azure": (240, 255, 255),
        "Beige": (245, 245, 220),
        "Bisque": (255, 228, 196),
        "Black": (0, 0, 0),
        "BlanchedAlmond": (255, 235, 205),
        "Blue": (0, 0, 255),
        "BlueViolet": (138, 43, 226),
        "Brown": (165, 42, 42),
        "BurlyWood": (222, 184, 135),
        "CadetBlue": (95, 158, 160),
        "Chartreuse": (127, 255, 0),
        "Chocolate": (210, 105, 30),
        "Coral": (255, 127, 80),
        "CornFlowerBlue": (100, 149, 237),
        "Cornsilk": (255, 248, 220),
        "Crimson": (220, 20, 60),
        "Cyan": (0, 255, 255),
        "DarkBlue": (0, 0, 139),
        "DarkCyan": (0, 139, 139),
        "DarkGoldenRod": (184, 134, 11),
        "DarkGray": (169, 169, 169),
        "DarkGreen": (0, 100, 0),
        "DarkKhaki": (189, 183, 107),
        "DarkMagenta": (139, 0, 139),
        "DarkOliveGreen": (85, 107, 47),
        "DarkOrange": (255, 140, 0),
        "DarkOrchid": (153, 50, 204),
        "DarkRed": (139, 0, 0),
        "DarkSalmon": (233, 150, 122),
        "DarkSeaGreen": (143, 188, 143),
        "DarkSlateBlue": (72, 61, 139),
        "DarkSlateGray": (47, 79, 79),
        "DarkTurquoise": (0, 206, 209),
        "DarkViolet": (148, 0, 211),
        "DeepPink": (255, 20, 147),
        "DeepSkyBlue": (0, 191, 255),
        "DimGray": (105, 105, 105),
        "DodgerBlue": (30, 144, 255),
        "FireBrick": (178, 34, 34),
        "FloralWhite": (255, 250, 240),
        "ForestGreen": (34, 139, 34),
        "Fuchsia": (255, 0, 255),
        "Gainsboro": (220, 220, 220),
        "GhostWhite": (248, 248, 255),
        "Gold": (255, 215, 0),
        "GoldenRod": (218, 165, 32),
        "Gray": (128, 128, 128),
        "Green": (0, 128, 0),
        "GreenYellow": (173, 255, 47),
        "HoneyDew": (240, 255, 240),
        "HotPink": (255, 105, 180),
        "IndianRed": (205, 92, 92),
        "Indigo": (75, 0, 130),
        "Ivory": (255, 255, 240),
        "Khaki": (240, 230, 140),
        "Lavender": (230, 230, 250),
        "LavenderBlush": (255, 240, 245),
        "LawnGreen": (124, 252, 0),
        "LemonChiffon": (255, 250, 205),
        "LightBlue": (173, 216, 230),
        "LightCoral": (240, 128, 128),
        "LightCyan": (224, 255, 255),
        "LightGoldenrodYellow": (250, 250, 210),
        "LightGray": (211, 211, 211),
        "LightGreen": (144, 238, 144),
        "LightPink": (255, 182, 193),
        "LightSalmon": (255, 160, 122),
        "LightSeaGreen": (32, 178, 170),
        "LightSkyBlue": (135, 206, 250),
        "LightSlateGray": (119, 136, 153),
        "LightSteelBlue": (176, 196, 222),
        "LightYellow": (255, 255, 224),
        "Lime": (0, 255, 0),
        "LimeGreen": (50, 205, 50),
        "Linen": (250, 240, 230),
        "Magenta": (255, 0, 255),
        "Maroon": (128, 0, 0),
        "MediumAquaMarine": (102, 205, 170),
        "MediumBlue": (0, 0, 205),
        "MediumOrchid": (186, 85, 211),
        "MediumPurple": (147, 112, 219),
        "MediumSeaGreen": (60, 179, 113),
        "MediumSlateBlue": (123, 104, 238),
        "MediumSpringGreen": (0, 250, 154),
        "MediumTurquoise": (72, 209, 204),
        "MediumVioletRed": (199, 21, 133),
        "MidnightBlue": (25, 25, 112),
        "MintCream": (245, 255, 250),
        "MistyRose": (255, 228, 225),
        "Moccasin": (255, 228, 181),
        "NavajoWhite": (255, 222, 173),
        "Navy": (0, 0, 128),
        "OldLace": (253, 245, 230),
        "Olive": (128, 128, 0),
        "OliveDrab": (107, 142, 35),
        "Orange": (255, 165, 0),
        "OrangeRed": (255, 69, 0),
        "Orchid": (218, 112, 214),
        "PaleGoldenRod": (238, 232, 170),
        "PaleGreen": (152, 251, 152),
        "PaleTurquoise": (175, 238, 238),
        "PaleVioletRed": (219, 112, 147),
        "PapayaWhip": (255, 239, 213),
        "PeachPuff": (255, 218, 185),
        "Peru": (205, 133, 63),
        "Pink": (255, 192, 203),
        "Plum": (221, 160, 221),
        "PowderBlue": (176, 224, 230),
        "Purple": (128, 0, 128),
        "Red": (255, 0, 0),
        "RosyBrown": (188, 143, 143),
        "RoyalBlue": (65, 105, 225),
        "SaddleBrown": (139, 69, 19),
        "Salmon": (250, 128, 114),
        "SandyBrown": (244, 164, 96),
        "SeaGreen": (46, 139, 87),
        "SeaShell": (255, 245, 238),
        "Sienna": (160, 82, 45),
        "Silver": (192, 192, 192),
        "SkyBlue": (135, 206, 235),
        "SlateBlue": (106, 90, 205),
        "SlateGray": (112, 128, 144),
        "Snow": (255, 250, 250),
        "SpringGreen": (0, 255, 127),
        "SteelBlue": (70, 130, 180),
        "Tan": (210, 180, 140),
        "Teal": (0, 128, 128),
        "Thistle": (216, 191, 216),
        "Tomato": (255, 99, 71),
        "Turquoise": (64, 224, 208),
        "Violet": (238, 130, 238),
        "Wheat": (245, 222, 179),
        "White": (255, 255, 255),
        "WhiteSmoke": (245, 245, 245),
        "Yellow": (255, 255, 0),
        "YellowGreen": (154, 205, 50),
    },
}


@dataclass
class ColorDetectionOutput(object):
    color_scheme: Dict[str, float]
    image: Optional[PilImage] = None


def get_color_names(ncolors: NColorType) -> Dict[str, Tuple[int, int, int]]:
    try:
        return COLORS[ncolors]
    except KeyError:
        raise ValueError("Invalid value for 'ncolors'. Value must be 16 or 140.")


def map_indices_to_color_names(closest_color_indices, colors) -> List[str]:
    colorscheme = []

    # Map the indices to color names
    for row_indices in closest_color_indices:
        row_colors = [list(colors.keys())[index] for index in row_indices]
        colorscheme.extend(row_colors)

    return colorscheme


def get_colors_w3c(
    img: PilImage,
    n_colors: NColorType = 16,
    is_plot: bool = False,
    plotncolors: int = 5,
) -> ColorDetectionOutput:
    """This functions is used to get a simplified color palette (W3C colors).
    It can be used with 16 (https://www.html-color-names.com/basic-color-names.php) or 140 colors (https://www.w3schools.com/colors/colors_names.asp)

    F = 255
    C0 = 192
    80 = 128

    :param img: image to analyze in RGB
    :type img: numpy.ndarray
    :param ncolors: number of colors to use
    :type ncolors: int
    :param plot: whether to plot a color pallette image
    :type plot: boolean
    :param plotncolors: number of colors to use in the pallette image
    :type plotncolors: int
    :return: percentage distribution of colors according to the W3C sixteens basic colors
    :rtype: list of shape ncolors x 2, where x[0] is the color name and x[1] the percentage of pixels most similar to that color in the image
    """
    assert img.mode == "RGB", "Image must be in RGB mode"

    img_arr = np.array(img)

    colors = get_color_names(n_colors)

    colors_array = np.array(list(colors.values()))

    dists = np.sum(np.abs(img_arr[:, :, np.newaxis, :3] - colors_array), axis=3)
    closest_color_indices = np.argmin(dists, axis=2)

    color_names = map_indices_to_color_names(closest_color_indices, colors)

    if img_arr.shape[2] == 4:
        alpha = img_arr[:, :, 3]
        # Exclude completely transparent pixels (alpha == 0) from distance calculation
        mask = alpha > 100
        mask = mask.ravel()
        color_names = np.array(color_names)[mask].tolist()

    unique_colors, counts = np.unique(color_names, return_counts=True)
    colorscheme = {
        c: count / len(color_names) * 100 for c, count in zip(unique_colors, counts)
    }

    missingcolors = list(set(colors) - set(unique_colors))
    for color in missingcolors:
        colorscheme[color] = 0.0

    colorscheme = {k: v for k, v in sorted(colorscheme.items())}

    if is_plot:
        import matplotlib.patches as patches
        import matplotlib.pyplot as plt

        sorted_data = sorted(colorscheme.items(), key=lambda x: x[1], reverse=True)

        fig, ax = plt.subplots()
        fig.suptitle(f"Top {plotncolors} colors ({n_colors} colors mode)")

        for i in range(0, plotncolors):
            ax.add_patch(
                patches.Rectangle((i, 0), 1, 1, facecolor=sorted_data[i][0].lower())
            )
        ax.set_xlim(0, plotncolors)

        buf = io.BytesIO()
        fig.savefig(buf, format="png")
        plt.close(fig)
        buf.seek(0)
        plot_img = Image.open(buf).convert("RGB")

        return ColorDetectionOutput(color_scheme=colorscheme, image=plot_img)

    else:
        return ColorDetectionOutput(color_scheme=colorscheme)
