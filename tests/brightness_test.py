import numpy as np
import pytest
from PIL import Image
from PIL.Image import Image as PilImage

from pyaesthetics.brightness import (
    get_relative_luminance_bt601,
    get_relative_luminance_bt709,
)
from pyaesthetics.utils import PyaestheticsTestCase


class TestBrightness(PyaestheticsTestCase):
    @pytest.fixture
    def image_filename(self) -> str:
        return "sample.jpg"

    @pytest.fixture
    def image(self, image_filename: str) -> PilImage:
        img_path = self.FIXTURES_ROOT / image_filename
        img = Image.open(img_path)
        return img

    def test_relative_luminance_bt601(self, image):
        brigtness = get_relative_luminance_bt601(image)
        assert not isinstance(brigtness, np.floating)
        assert pytest.approx(brigtness, 0.0001) == 0.6024

    def test_relative_luminance_bt709(self, image):
        brigtness = get_relative_luminance_bt709(image)
        assert not isinstance(brigtness, np.floating)
        assert pytest.approx(brigtness, 0.0001) == 0.5918
