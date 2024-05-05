import cv2
import pytest
from PIL import Image

from pyaesthetics.colorfulness import colorfulness_hsv, colorfulness_rgb
from pyaesthetics.utils import PyaestheticsTestCase


class TestColorfulness(PyaestheticsTestCase):
    @pytest.fixture
    def image(self):
        sample_image_path = str(self.FIXTURES_ROOT / "sample.jpg")
        return Image.open(sample_image_path)

    def test_colorfulness_hsv(self, image):
        c = colorfulness_hsv(image)
        assert pytest.approx(c, 0.0001) == 140.2441

    def test_colorfulness_rgb(self, image):
        c = colorfulness_rgb(image)
        assert pytest.approx(c, 0.0001) == 73.8137
