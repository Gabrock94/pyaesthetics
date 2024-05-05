import pytest
from PIL import Image
from PIL.Image import Image as PilImage

from pyaesthetics.symmetry import get_symmetry
from pyaesthetics.utils import PyaestheticsTestCase


class TestSymmetry(PyaestheticsTestCase):
    @pytest.mark.parametrize(
        argnames="min_std, min_size, expected_result",
        argvalues=(
            (
                5,
                20,
                74.43491816056118,  # 60.747663551401864,
            ),
        ),
    )
    def test_symmetry(self, min_std: int, min_size: int, expected_result: float):
        sample_image_path = str(self.FIXTURES_ROOT / "sample.jpg")
        img = Image.open(sample_image_path)
        output = get_symmetry(img, min_std=min_std, min_size=min_size)
        actual_result = output.degree
        assert actual_result == expected_result
        assert output.images is None

    @pytest.mark.parametrize(
        argnames="min_std, min_size",
        argvalues=((5, 20),),
    )
    def test_plot(self, min_std: int, min_size: int):
        sample_image_path = str(self.FIXTURES_ROOT / "sample.jpg")
        img = Image.open(sample_image_path)
        output = get_symmetry(img, min_std=min_std, min_size=min_size, is_plot=True)
        assert output.images is not None

        assert isinstance(output.images.left, PilImage)
        assert isinstance(output.images.right, PilImage)
