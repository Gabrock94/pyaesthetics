import pytest
from PIL import Image

from pyaesthetics.analysis import analyze_image
from pyaesthetics.utils import PyaestheticsTestCase


class TestAnalysis(PyaestheticsTestCase):
    @pytest.mark.parametrize(
        argnames="method",
        argvalues=("complete", "fast"),
    )
    def test_analyze_image(self, method: str):
        sample_image_path = str(self.FIXTURES_ROOT / "sample2.jpg")
        image = Image.open(sample_image_path)
        analyze_image(image, method=method)
