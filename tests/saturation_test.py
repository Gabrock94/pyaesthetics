import numpy as np
import pytest
from PIL import Image

from pyaesthetics.saturation import get_saturation
from pyaesthetics.utils import PyaestheticsTestCase


class TestSaturation(PyaestheticsTestCase):
    @pytest.mark.parametrize(
        argnames="image_filename, expected_result",
        argvalues=(
            ("800px-Multi-color_leaf_without_saturation.jpg", 0.3141780693533271),
            ("800px-Multi-color_leaf_with_saturation.jpg", 0.5300632097800362),
        ),
    )
    def test_saturation(self, image_filename: str, expected_result: float):
        sample_image_path = str(self.FIXTURES_ROOT / image_filename)
        img = Image.open(sample_image_path)
        actual_result = get_saturation(img)
        assert not isinstance(actual_result, np.floating)
        assert expected_result == actual_result
