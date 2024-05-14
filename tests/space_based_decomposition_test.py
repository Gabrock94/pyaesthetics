import pytest
from PIL import Image
from PIL.Image import Image as PilImage

from pyaesthetics.space_based_decomposition import (
    AreaCoordinates,
    AreaOutput,
    AreasOutput,
    TextImageRatioOutput,
    get_areas,
    get_text_image_ratio,
)
from pyaesthetics.utils import PyaestheticsTestCase


class TestSpaceBasedDecomposition(PyaestheticsTestCase):
    @pytest.fixture
    def image_filename(self) -> str:
        return "sample2.jpg"

    @pytest.fixture
    def image(self, image_filename: str) -> PilImage:
        sample_image_path = str(self.FIXTURES_ROOT / image_filename)
        return Image.open(sample_image_path)

    def test_get_areas(self, image: PilImage):
        actual = get_areas(
            image,
            is_plot=True,
            is_coordinates=True,
            is_areatype=True,
        )
        expected = AreasOutput(
            areas=[
                AreaOutput(
                    area=881720,
                    coordinates=AreaCoordinates(xmin=70, xmax=1008, ymin=67, ymax=1007),
                    area_type="Image",
                ),
                AreaOutput(
                    area=4104,
                    coordinates=AreaCoordinates(xmin=801, xmax=972, ymin=629, ymax=653),
                    area_type="Text",
                ),
                AreaOutput(
                    area=312,
                    coordinates=AreaCoordinates(xmin=948, xmax=972, ymin=86, ymax=99),
                    area_type="Image",
                ),
                AreaOutput(
                    area=2989,
                    coordinates=AreaCoordinates(
                        xmin=961, xmax=1022, ymin=974, ymax=1023
                    ),
                    area_type="Image",
                ),
            ],
            image=Image.new("RGB", size=(image.width, image.height), color="white"),
        )
        assert len(actual.areas) == len(expected.areas)

        for actual_area, expected_area in zip(actual.areas, expected.areas):
            assert actual_area.area == expected_area.area

    def test_get_text_image_ratio(self, image: PilImage):
        areas = get_areas(image, is_plot=True, is_coordinates=True, is_areatype=True)

        actual = get_text_image_ratio(areas)
        expected = TextImageRatioOutput(
            text_image_ratio=0.004615773935048503,
            text_area=4104,
            image_area=885021,
            num_areas=3,
        )
        assert actual == expected
