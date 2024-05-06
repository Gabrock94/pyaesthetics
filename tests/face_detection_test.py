import numpy as np
import pytest
from PIL import Image

from pyaesthetics.face_detection import get_faces
from pyaesthetics.utils import PyaestheticsTestCase


class TestFaceDetection(PyaestheticsTestCase):
    @pytest.mark.parametrize(argnames="is_plot", argvalues=(True, False))
    def test_get_faces(self, is_plot: bool):
        sample_image_path = str(
            self.FIXTURES_ROOT / "turing-2018-bengio-hinton-lecun.jpg"
        )
        img = Image.open(sample_image_path)
        output = get_faces(img, is_plot=is_plot)
        assert len(output.bboxes) == 3
        assert not isinstance(output.bboxes, np.ndarray)

        if is_plot:
            assert output.images is not None
            assert len(output.images) == len(output.bboxes)
        else:
            assert output.images is None
