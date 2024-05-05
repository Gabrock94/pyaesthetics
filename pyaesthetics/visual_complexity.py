import io
from dataclasses import dataclass
from typing import Optional

from PIL.Image import Image as PilImage

from pyaesthetics.utils import QuadTreeDecomposer


@dataclass
class VisualComplexityOutput(object):
    num_blocks: int
    weight: Optional[int] = None


def get_visual_complexity(
    img: PilImage, min_std: int, min_size: int, is_weight: bool = False
) -> VisualComplexityOutput:
    assert img.mode == "RGB", f"Image must be in RGB mode but is in {img.mode}"

    def get_num_blocks(img: PilImage, min_std: int, min_size: int) -> int:
        quad_tree = QuadTreeDecomposer(img=img, min_std=min_std, min_size=min_size)
        return len(quad_tree.blocks)

    def get_weight(img: PilImage) -> int:
        img_io = io.BytesIO()

        # Here it is assumed that non-PNG image formats may be input,
        # but always save in PNG format and calculate their weight (size) to
        # keep the output consistent.
        img.save(img_io, format="PNG")
        # Seek to the end fo the file
        img_io.seek(0, 2)

        return img_io.tell()

    return VisualComplexityOutput(
        num_blocks=get_num_blocks(img=img, min_std=min_std, min_size=min_size),
        weight=get_weight(img) if is_weight else None,
    )
