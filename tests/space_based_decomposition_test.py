from PIL import Image

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
    def test_get_areas(self):
        sample_image_path = str(self.FIXTURES_ROOT / "sample2.jpg")
        img = Image.open(sample_image_path)

        actual = get_areas(
            img,
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
            image=Image.new("RGB", size=(img.width, img.height), color="white"),
        )
        for actual_area, expected_area in zip(actual.areas, expected.areas):
            assert actual_area.area == expected_area.area

    def test_get_text_image_ratio(self):
        sample_image_path = str(self.FIXTURES_ROOT / "sample2.jpg")
        img = Image.open(sample_image_path)
        areas = get_areas(img, is_plot=True, is_coordinates=True, is_areatype=True)

        actual = get_text_image_ratio(areas)
        expected = TextImageRatioOutput(
            text_image_ratio=0.004615773935048503,
            text_area=4104,
            image_area=885021,
            num_areas=3,
        )
        assert actual == expected
