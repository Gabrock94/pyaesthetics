import numpy as np
import pytest
from PIL import Image

from pyaesthetics.contrast import contrast_michelson, contrast_rms
from pyaesthetics.utils import PyaestheticsTestCase


class TestContrast(PyaestheticsTestCase):
    @pytest.mark.parametrize(
        argnames="image_filename, expected_result",
        argvalues=(
            ("800px-Multi-color_leaf_without_saturation.jpg", 0.13328748035416788),
            ("800px-Multi-color_leaf_with_saturation.jpg", 0.15157391276137983),
        ),
    )
    def test_contrast_rms(self, image_filename: str, expected_result: float):
        sample_image_path = str(self.FIXTURES_ROOT / image_filename)
        img = Image.open(sample_image_path)
        actual_result = contrast_rms(img)
        assert not isinstance(actual_result, np.floating)
        assert actual_result == expected_result

    @pytest.mark.parametrize(
        argnames="image_filename, expected_result",
        argvalues=(
            ("800px-Multi-color_leaf_without_saturation.jpg", 0.9829059829059829),
            ("800px-Multi-color_leaf_with_saturation.jpg", 0.9921875),
        ),
    )
    def test_contrast_michelson(self, image_filename: str, expected_result: float):
        sample_image_path = str(self.FIXTURES_ROOT / image_filename)
        img = Image.open(sample_image_path)
        actual_result = contrast_michelson(img)
        assert not isinstance(actual_result, np.floating)
        assert actual_result == expected_result
