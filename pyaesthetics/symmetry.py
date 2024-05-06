#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to compute the degree of symmetry of an image.
- Symmetry by QuadTree Decomposition

Created on Mon Apr 16 11:49:45 2018

@author: giulio
"""

import os
from dataclasses import dataclass
from typing import Optional

import numpy as np
from PIL import Image
from PIL.Image import Image as PilImage

from pyaesthetics.utils import QuadTreeDecomposer

###############################################################################
#                                                                             #
#                                  Symmetry                                   #
#                                                                             #
###############################################################################
""" Thìs sections handles Quadratic Tree Decomposition. """


@dataclass
class SymmetryImage(object):
    left: PilImage
    right: PilImage

    def save_images(self, save_dir_path: str = "."):
        self.left.save(os.path.join(save_dir_path, "left.png"))
        self.right.save(os.path.join(save_dir_path, "right.png"))


@dataclass
class SymmetryOutput(object):
    degree: float
    images: Optional[SymmetryImage] = None


def get_symmetry(img: PilImage, min_std: int, min_size: int, is_plot: bool = False):
    """This function returns the degree of symmetry (0-100) between the left and right side of an image

    :param img: img to analyze
    :type img: numpy.ndarray
    :minStd: Std threshold for subsequent splitting
    :type minStd: int
    :minSize: Size threshold for subsequent splitting, in pixel
    :type minStd: int
    :return: degree of vertical symmetry
    :rtype: float
    """
    assert img.mode == "RGB", f"Image must be in RGB mode but is in {img.mode}"
    img_arr = np.array(img)

    h, w, _ = img_arr.shape
    assert img.size == (w, h)

    if h % 2 != 0:
        img_arr = img_arr[:-1, :]
    if w % 2 != 0:
        img_arr = img_arr[:, :-1]

    img_arr_l = img_arr[0:, 0 : int(w / 2)]
    img_arr_r = np.flip(img_arr[0:, int(w / 2) :], 1)

    img_l = Image.fromarray(img_arr_l)
    img_r = Image.fromarray(img_arr_r)

    tree_l = QuadTreeDecomposer(img=img_l, min_std=min_std, min_size=min_size)
    tree_r = QuadTreeDecomposer(img=img_r, min_std=min_std, min_size=min_size)

    blocks_l = tree_l.decompose(x=0, y=0)
    blocks_r = tree_r.decompose(x=0, y=0)

    counter = 0
    tot = len(blocks_r) + len(blocks_l)
    for block_r in blocks_r:
        for block_l in blocks_l:
            if block_r.to_coordinates() == block_l.to_coordinates():
                counter += 1
    degree = counter / tot * 200

    images = (
        SymmetryImage(left=tree_l.get_plot(), right=tree_r.get_plot())
        if is_plot
        else None
    )

    return SymmetryOutput(degree=degree, images=images)
