# -*- coding: utf-8 -*-

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This module contains functions to compute the number of indipendent areas in an image.

Created on Sat Apr 21 09:40:45 2018

@author: giulio
"""

from dataclasses import dataclass
from typing import List, Literal, Optional

import cv2
import numpy as np
from imutils import contours, perspective
from PIL import Image
from PIL.Image import Image as PilImage

from pyaesthetics.utils import detect_text

###############################################################################
#                                                                             #
#                                  Symmetry                                   #
#                                                                             #
###############################################################################
""" Thìs sections handles Quadratic Tree Decomposition. """

AreaType = Literal["Text", "Image"]


@dataclass
class AreaCoordinates(object):
    xmin: int
    xmax: int
    ymin: int
    ymax: int


@dataclass
class AreaOutput(object):
    area: int
    coordinates: Optional[AreaCoordinates] = None
    area_type: Optional[AreaType] = None


@dataclass
class AreasOutput(object):
    areas: List[AreaOutput]
    image: Optional[PilImage] = None


@dataclass
class TextImageRatioOutput(object):
    text_image_ratio: float
    text_area: int
    image_area: int
    num_areas: int


def get_text_image_ratio(areas_output: AreasOutput) -> TextImageRatioOutput:
    """This function evaluates the text on image ration, as well as the total area occupied by both image and text.

    :param areas: areas dict as extracted by the getAreas function
    :type areas: dict
    :return: a dict containing the text / (image+text) ratio , total area of text and total area of images and number of images
    :rtype: dict
    """
    image, text = [], []

    for area in areas_output.areas:
        if area.area_type == "Text":
            text.append(area.area)
        elif area.area_type == "Image":
            image.append(area.area)

    # ratio is 0.5 if picture and text occupy the same area, more in more text, less if more images.
    ratio = sum(text) / (sum(image) + sum(text))

    return TextImageRatioOutput(
        text_image_ratio=ratio,
        text_area=sum(text),
        image_area=sum(image),
        num_areas=len(image),
    )


def get_areas(
    img: PilImage,
    min_area: int = 100,
    is_resize: bool = True,
    new_size=[600, 400],
    is_plot: bool = False,
    is_coordinates: bool = False,
    is_areatype: bool = False,
) -> AreasOutput:
    """Adapted from https://www.pyimagesearch.com/2016/03/28/measuring-size-of-objects-in-an-image-with-opencv/"""
    assert img.mode == "RGB", f"Image must be in RGB mode but is in {img.mode}"
    img_arr = np.array(img)

    img_original_arr = img_arr.copy()  # source of the image
    oh, ow, _ = img_original_arr.shape  # shape of the orignal image
    assert img.size == (ow, oh)

    img_arr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)  # conversion to greyscale

    if is_resize:
        img_arr = cv2.resize(
            img_arr, new_size, interpolation=cv2.INTER_CUBIC
        )  # resizing

    img_arr = cv2.GaussianBlur(img_arr, (3, 3), 0)  # apply a Gaussina filter
    edged = cv2.Canny(img_arr, 10, 100)
    edged = cv2.dilate(edged, kernel=None, iterations=1)  # type: ignore

    edged = cv2.erode(edged, kernel=None, iterations=1)  # type: ignore

    # get the contours
    cnts, _ = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(cnts) < 1:
        return AreasOutput(areas=[])

    (cnts, _) = contours.sort_contours(cnts)

    def get_bboxes_from_contours(cnts: List[np.ndarray]):
        bboxes = []
        for cnt in cnts:  # for each contour
            min_area_rect = cv2.minAreaRect(cnt)
            min_area_rect_arr = cv2.boxPoints(min_area_rect)
            min_area_rect_arr = min_area_rect_arr.astype("int")
            min_area_rect_arr = perspective.order_points(min_area_rect_arr)
            min_area_rect_arr = min_area_rect_arr.astype("int")

            if is_resize:
                # convert the box to the size of the original image
                min_area_rect_arr = np.array(
                    [
                        [
                            int(corner[0] * ow / new_size[0]),
                            int(corner[1] * oh / new_size[1]),
                        ]
                        for corner in min_area_rect_arr
                    ]
                )
            else:
                # convert the box to the size of the original image
                min_area_rect_arr = np.array(
                    [[int(corner[0]), int(corner[1])] for corner in min_area_rect_arr]
                )
            bboxes.append(min_area_rect_arr)
        return bboxes

    def plot_contours(img_arr: np.ndarray, bboxes: List[np.ndarray]) -> PilImage:
        for bbox in bboxes:
            cv2.drawContours(img_arr, [bbox], -1, (0, 255, 0), 2)
        return Image.fromarray(img_arr)

    bboxes = get_bboxes_from_contours(cnts)  # type: ignore
    plot_img = plot_contours(img_original_arr, bboxes) if is_plot else None  # type: ignore

    """ Now, we can calculate the area of each box, and we can detect if some text is present"""
    areas = []

    def get_area_type(is_areatype: bool, imgportion: np.ndarray) -> Optional[AreaType]:
        if not is_areatype:
            return None

        num_texts = detect_text(Image.fromarray(imgportion))
        return "Text" if num_texts > 0 else "Image"

    def get_area_coordinates(
        is_coordinates: bool, xmin: int, xmax: int, ymin: int, ymax: int
    ) -> Optional[AreaCoordinates]:
        if not is_coordinates:
            return None

        return AreaCoordinates(xmin=xmin, xmax=xmax, ymin=ymin, ymax=ymax)

    for bbox in bboxes:
        t = np.transpose(bbox)
        xmin, xmax = min(t[0]), max(t[0])
        ymin, ymax = min(t[1]), max(t[1])
        area = (xmax - xmin) * (ymax - ymin)

        if area <= min_area:
            continue

        imgportion = img_original_arr[ymin:ymax, xmin:xmax]
        if imgportion.size == 0:
            continue

        area_type = get_area_type(is_areatype, imgportion)
        area_coordinates = get_area_coordinates(
            is_coordinates=is_coordinates,
            xmin=xmin.item(),
            xmax=xmax.item(),
            ymin=ymin.item(),
            ymax=ymax.item(),
        )

        areas.append(
            AreaOutput(
                area=area.item(),
                coordinates=area_coordinates,
                area_type=area_type,
            )
        )

    return AreasOutput(areas=areas, image=plot_img)
