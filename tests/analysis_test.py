from typing import get_args

import pytest
from PIL import Image

from pyaesthetics.analysis import AnalyzeMethod, analyze_image
from pyaesthetics.utils import PyaestheticsTestCase


class TestAnalysis(PyaestheticsTestCase):
    @pytest.mark.parametrize(
        argnames="method",
        argvalues=get_args(AnalyzeMethod),
    )
    def test_analyze_image(self, method: AnalyzeMethod):
        sample_image_path = str(self.FIXTURES_ROOT / "sample2.jpg")
        image = Image.open(sample_image_path)
        analyze_image(image, method=method)
