import numpy as np
import pytest
from PIL import Image
from PIL.Image import Image as PilImage

from pyaesthetics.face_detection import get_faces
from pyaesthetics.utils import PyaestheticsTestCase


class TestFaceDetection(PyaestheticsTestCase):
    @pytest.fixture
    def image_filename(self) -> str:
        return "turing-2018-bengio-hinton-lecun.jpg"

    @pytest.fixture
    def image(self, image_filename: str) -> PilImage:
        sample_image_path = str(self.FIXTURES_ROOT / image_filename)
        return Image.open(sample_image_path)

    @pytest.mark.parametrize(argnames="is_plot", argvalues=(True, False))
    def test_get_faces(self, image: PilImage, is_plot: bool):
        output = get_faces(image, is_plot=is_plot)
        assert len(output.bboxes) == 3
        assert not isinstance(output.bboxes, np.ndarray)

        if is_plot:
            assert output.images is not None
            assert len(output.images) == len(output.bboxes)
        else:
            assert output.images is None
