from typing import get_args

import pytest
from PIL import Image

from pyaesthetics.analysis import AnalyzeMethod, ImageAnalysisOutput, analyze_image
from pyaesthetics.utils import PyaestheticsTestCase


class TestAnalysis(PyaestheticsTestCase):
    @pytest.fixture
    def image_filename(self) -> str:
        return "sample2.jpg"

    @pytest.mark.parametrize(
        argnames="method",
        argvalues=get_args(AnalyzeMethod),
    )
    def test_analyze_image(self, method: AnalyzeMethod, image_filename: str):
        sample_image_path = str(self.FIXTURES_ROOT / image_filename)
        image = Image.open(sample_image_path)
        output = analyze_image(image, method=method)
        assert isinstance(output, ImageAnalysisOutput)
