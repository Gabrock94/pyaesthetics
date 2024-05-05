from dataclasses import dataclass, field
from typing import List, Optional, Tuple

import cv2
import numpy as np
from PIL import ImageDraw
from PIL.Image import Image as PilImage


@dataclass
class DecomposeOutput(object):
    x: int
    y: int
    w: int
    h: int
    std: int

    @property
    def l(self) -> int:
        return self.x

    @property
    def t(self) -> int:
        return self.y

    @property
    def r(self) -> int:
        return self.x + self.w

    @property
    def b(self) -> int:
        return self.y + self.h

    def to_coordinates(self) -> Tuple[int, int, int, int]:
        return self.x, self.y, self.w, self.h


@dataclass
class QuadTreeDecomposer(object):
    """This class is used to perfrom a QuadTree decomposition of an image.

    During initialization, QuadTree decomposition is done and result are store in self.blocks as a list containing [x, y, w, h , std].

    To visualize the results, use get_plot().
    """

    min_std: int
    min_size: int
    img: PilImage

    _img_arr: Optional[np.ndarray] = field(default=None, repr=False)
    _blocks: Optional[List[DecomposeOutput]] = field(default=None, repr=False)

    def __post_init__(self) -> None:
        assert (
            self.img.mode == "RGB"
        ), f"Image must be in RGB mode but is in {self.img.mode} mode"
        img_arr = np.array(self.img)
        self._img_arr = cv2.cvtColor(img_arr, cv2.COLOR_RGB2GRAY)

    @property
    def img_arr(self) -> np.ndarray:
        assert self._img_arr is not None
        return self._img_arr

    @property
    def blocks(self) -> List[DecomposeOutput]:
        if self._blocks is None:
            self._blocks = self.decompose(x=0, y=0)
        return self._blocks

    def get_plot(self, edgecolor="red", linewidth=1) -> PilImage:
        blocks = self.blocks
        img = self.img.copy()
        draw = ImageDraw.Draw(img)

        for block in blocks:
            xy = (block.l, block.t, block.r, block.b)
            draw.rectangle(xy=xy, outline=edgecolor, width=linewidth)

        return img

    def decompose(self, x: int, y: int) -> List[DecomposeOutput]:
        return list(self._decompose(self.img_arr, x, y))

    def _decompose(self, img: np.ndarray, x: int, y: int):
        """This function evaluate the mean and std of an image, and decides Whether to perform or not other 2 splits of the leave.

        :param img: img to analyze
        :type img: numpy.ndarray
        :param x: x offset of the leaves to analyze
        :type x: int
        :param Y: Y offset of the leaves to analyze
        :type Y: int
        """

        w, h = img.shape
        std = int(img.std())

        if std >= self.min_std and max(w, h) >= self.min_size:
            if w >= h:
                w2 = int(w / 2)
                img1 = img[0:w2, 0:h]
                img2 = img[w2:, 0:h]
                yield from self._decompose(img1, x, y)
                yield from self._decompose(img2, x + w2, y)
            else:
                h2 = int(h / 2)
                img1 = img[0:, 0:h2]
                img2 = img[0:, h2:]
                yield from self._decompose(img1, x, y)
                yield from self._decompose(img2, x, y + h2)

        yield DecomposeOutput(x=x, y=y, w=w, h=h, std=std)
