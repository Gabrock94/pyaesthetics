import pytest
from PIL import Image
from PIL.Image import Image as PilImage

from pyaesthetics.utils import PyaestheticsTestCase
from pyaesthetics.visual_complexity import get_visual_complexity


class TestVisualComplexity(PyaestheticsTestCase):
    @pytest.fixture
    def image(self) -> PilImage:
        img_path = self.FIXTURES_ROOT / "sample.jpg"
        img = Image.open(img_path)
        return img

    def test_get_visual_complexity(self, image):
        output = get_visual_complexity(
            img=image, min_std=15, min_size=40, is_weight=True
        )
        assert output.num_blocks == 781
        assert output.weight == 271547
