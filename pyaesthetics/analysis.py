"""
This is an entrypoint for the automatic analysis of images using pyaeshtetics.

@author: Giulio Gabrieli
"""

###############################################################################
#                                                                             #
#                                 Libraries                                   #
#                                                                             #
###############################################################################

from dataclasses import dataclass
from typing import Literal, Optional, Tuple, get_args

from PIL.Image import Image as PilImage

from pyaesthetics.brightness import (
    get_relative_luminance_bt601,
    get_relative_luminance_bt709,
)
from pyaesthetics.color_detection import ColorDetectionOutput, get_colors_w3c
from pyaesthetics.colorfulness import get_colorfulness_hsv, get_colorfulness_rgb
from pyaesthetics.contrast import contrast_michelson, contrast_rms
from pyaesthetics.face_detection import GetFacesOutput, get_faces
from pyaesthetics.saturation import get_saturation
from pyaesthetics.space_based_decomposition import (
    TextImageRatioOutput,
    get_areas,
    get_text_image_ratio,
)
from pyaesthetics.symmetry import SymmetryOutput, get_symmetry
from pyaesthetics.visual_complexity import VisualComplexityOutput, get_visual_complexity

###############################################################################
#                                                                             #
#                      Quadratic Tree Decomposition                           #
#                                                                             #
###############################################################################

AnalyzeMethod = Literal["fast", "complete"]


@dataclass
class Brightness(object):
    bt709: float
    bt601: Optional[float] = None


@dataclass
class Colorfulness(object):
    rgb: float
    hsv: Optional[float] = None


@dataclass
class Contrast(object):
    rms: float
    michelson: Optional[float] = None


@dataclass
class ImageAnalysisOutput(object):
    brightness: Brightness
    visual_complexity: VisualComplexityOutput
    symmetry: SymmetryOutput
    colorfulness: Colorfulness
    contrast: Contrast
    saturation: float

    faces: Optional[GetFacesOutput] = None
    colors: Optional[ColorDetectionOutput] = None
    text_image_ratio: Optional[TextImageRatioOutput] = None


def analyze_image_fast(
    img: PilImage,
    min_std: int,
    min_size: int,
) -> ImageAnalysisOutput:
    brightness = Brightness(
        bt709=get_relative_luminance_bt709(img),
    )
    visual_complexity = get_visual_complexity(
        img=img,
        min_std=min_std,
        min_size=min_size,
        is_weight=False,
    )
    symmetry = get_symmetry(
        img=img,
        min_std=min_std,
        min_size=min_size,
    )
    colorfulness = Colorfulness(
        rgb=get_colorfulness_rgb(img),
    )
    contrast = Contrast(
        rms=contrast_rms(img),
    )
    saturation = get_saturation(img)

    return ImageAnalysisOutput(
        brightness=brightness,
        visual_complexity=visual_complexity,
        symmetry=symmetry,
        colorfulness=colorfulness,
        contrast=contrast,
        saturation=saturation,
    )


def analyze_image_complete(
    img: PilImage,
    min_std: int,
    min_size: int,
    is_resize: bool,
    resized_w: int,
    resized_h: int,
) -> ImageAnalysisOutput:
    brightness = Brightness(
        bt709=get_relative_luminance_bt709(img),
        bt601=get_relative_luminance_bt601(img),
    )
    visual_complexity = get_visual_complexity(
        img=img,
        min_std=min_std,
        min_size=min_size,
        is_weight=True,
    )
    symmetry = get_symmetry(
        img=img,
        min_std=min_std,
        min_size=min_size,
    )
    colorfulness = Colorfulness(
        rgb=get_colorfulness_rgb(img),
        hsv=get_colorfulness_hsv(img),
    )
    contrast = Contrast(
        rms=contrast_rms(img),
        michelson=contrast_michelson(img),
    )
    saturation = get_saturation(img)

    faces = get_faces(img=img)
    colors = get_colors_w3c(img=img, n_colors=140)

    areas = get_areas(
        img,
        is_resize=is_resize,
        resized_w=resized_w,
        resized_h=resized_h,
        is_areatype=True,
    )
    text_image_ratio = get_text_image_ratio(areas)

    return ImageAnalysisOutput(
        brightness=brightness,
        visual_complexity=visual_complexity,
        symmetry=symmetry,
        colorfulness=colorfulness,
        contrast=contrast,
        saturation=saturation,
        faces=faces,
        colors=colors,
        text_image_ratio=text_image_ratio,
    )


def analyze_image(
    img: PilImage,
    method: AnalyzeMethod = "fast",
    is_resize: bool = True,
    resized_w: int = 600,
    resized_h: int = 400,
    min_std: int = 10,
    min_size: int = 20,
) -> ImageAnalysisOutput:
    """This functions act as entrypoint for the automatic analysis of an image aesthetic features.

    :param pathToImg: path to the image to analyze
    :type pathToImg: str
    :param method: set to analysis to use. Valid methods are 'fast','complete'. Default is 'fast'.
    :type pathToImg: str
    :param resize: indicate wether to resize the image (reduce computational workload, increase requested time)
    :type resize: boolean
    :param newSize: if the image has to be resized, this tuple indicates the new size of the image
    :type newSize: tuple
    :param minStd: minimum standard deviation for the Quadratic Tree Decomposition
    :type minStd: int
    :param minSize: minimum size for the Quadratic Tree Decomposition
    :type minSize: int
    :return: number of character in the text
    :rtype: dict

    """
    if method == "fast":
        return analyze_image_fast(
            img=img,
            min_std=min_std,
            min_size=min_size,
        )
    elif method == "complete":
        return analyze_image_complete(
            img=img,
            min_std=min_std,
            min_size=min_size,
            is_resize=is_resize,
            resized_w=resized_w,
            resized_h=resized_h,
        )
    else:
        raise ValueError(
            f"Invalid method {method}. Valid methods are {get_args(AnalyzeMethod)}"
        )
