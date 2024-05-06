import numpy as np
import pytest
from PIL import Image
from PIL.Image import Image as PilImage

from pyaesthetics.color_detection import get_colors_w3c
from pyaesthetics.utils import PyaestheticsTestCase


class TestColorDetection(PyaestheticsTestCase):
    @pytest.fixture
    def image(self) -> PilImage:
        sample_image_path = str(self.FIXTURES_ROOT / "sample.jpg")
        return Image.open(sample_image_path)

    @pytest.mark.parametrize(
        argnames="expected_results, n_colors",
        argvalues=(
            (
                {
                    "Aqua": 1.3901748971193415,
                    "Black": 0.28703703703703703,
                    "Blue": 0.06944444444444445,
                    "Fuchsia": 0.0,
                    "Gray": 35.45293209876543,
                    "Green": 0.0,
                    "Lime": 0.0,
                    "Maroon": 0.00102880658436214,
                    "Navy": 6.326646090534979,
                    "Olive": 0.0,
                    "Purple": 0.03446502057613169,
                    "Red": 0.0,
                    "Silver": 4.596450617283951,
                    "Teal": 2.112139917695473,
                    "White": 49.72968106995885,
                    "Yellow": 0.0,
                },
                16,
            ),
            (
                {
                    "AliceBlue": 1.65869341563786,
                    "AntiqueWhite": 0.32175925925925924,
                    "Aqua": 0.0,
                    "AquaMarine": 0.0,
                    "Azure": 0.15457818930041153,
                    "Beige": 0.00308641975308642,
                    "Bisque": 0.048868312757201646,
                    "Black": 0.03575102880658436,
                    "BlanchedAlmond": 0.15380658436213993,
                    "Blue": 0.0,
                    "BlueViolet": 0.0,
                    "Brown": 0.000771604938271605,
                    "BurlyWood": 0.00205761316872428,
                    "CadetBlue": 0.008487654320987654,
                    "Chartreuse": 0.0,
                    "Chocolate": 0.0,
                    "Coral": 0.0,
                    "CornFlowerBlue": 5.677983539094651,
                    "Cornsilk": 0.00102880658436214,
                    "Crimson": 0.0,
                    "Cyan": 0.0,
                    "DarkBlue": 0.000257201646090535,
                    "DarkCyan": 0.0,
                    "DarkGoldenRod": 0.0,
                    "DarkGray": 0.2716049382716049,
                    "DarkGreen": 0.0,
                    "DarkKhaki": 0.0,
                    "DarkMagenta": 0.000771604938271605,
                    "DarkOliveGreen": 0.000257201646090535,
                    "DarkOrange": 0.0,
                    "DarkOrchid": 0.00102880658436214,
                    "DarkRed": 0.0,
                    "DarkSalmon": 0.09079218106995886,
                    "DarkSeaGreen": 0.0,
                    "DarkSlateBlue": 5.848508230452675,
                    "DarkSlateGray": 0.25385802469135804,
                    "DarkTurquoise": 0.0,
                    "DarkViolet": 0.0,
                    "DeepPink": 0.0,
                    "DeepSkyBlue": 0.0,
                    "DimGray": 0.12242798353909465,
                    "DodgerBlue": 0.27649176954732513,
                    "FireBrick": 0.0,
                    "FloralWhite": 0.061213991769547324,
                    "ForestGreen": 0.0,
                    "Fuchsia": 0.0,
                    "Gainsboro": 0.537037037037037,
                    "GhostWhite": 4.135802469135803,
                    "Gold": 0.0,
                    "GoldenRod": 0.0,
                    "Gray": 0.06584362139917696,
                    "Green": 0.0,
                    "GreenYellow": 0.0,
                    "HoneyDew": 0.12602880658436214,
                    "HotPink": 1.504372427983539,
                    "IndianRed": 0.00205761316872428,
                    "Indigo": 0.002829218106995885,
                    "Ivory": 0.1280864197530864,
                    "Khaki": 0.0,
                    "Lavender": 2.848508230452675,
                    "LavenderBlush": 0.709619341563786,
                    "LawnGreen": 0.0,
                    "LemonChiffon": 0.000257201646090535,
                    "LightBlue": 0.04603909465020576,
                    "LightCoral": 0.4367283950617284,
                    "LightCyan": 0.05169753086419753,
                    "LightGoldenrodYellow": 0.0,
                    "LightGray": 0.3238168724279835,
                    "LightGreen": 0.0,
                    "LightPink": 0.9390432098765432,
                    "LightSalmon": 0.28420781893004116,
                    "LightSeaGreen": 0.000257201646090535,
                    "LightSkyBlue": 0.397119341563786,
                    "LightSlateGray": 0.3212448559670782,
                    "LightSteelBlue": 0.3096707818930041,
                    "LightYellow": 0.0,
                    "Lime": 0.0,
                    "LimeGreen": 0.0,
                    "Linen": 0.15997942386831276,
                    "Magenta": 0.0,
                    "Maroon": 0.0,
                    "MediumAquaMarine": 0.0,
                    "MediumBlue": 0.0,
                    "MediumOrchid": 0.006687242798353909,
                    "MediumPurple": 2.078960905349794,
                    "MediumSeaGreen": 0.0,
                    "MediumSlateBlue": 14.37551440329218,
                    "MediumSpringGreen": 0.0,
                    "MediumTurquoise": 0.0,
                    "MediumVioletRed": 0.000771604938271605,
                    "MidnightBlue": 2.7170781893004117,
                    "MintCream": 0.25462962962962965,
                    "MistyRose": 0.330761316872428,
                    "Moccasin": 0.0,
                    "NavajoWhite": 0.0,
                    "Navy": 0.007458847736625513,
                    "OldLace": 0.0038580246913580245,
                    "Olive": 0.0,
                    "OliveDrab": 0.0,
                    "Orange": 0.0,
                    "OrangeRed": 0.0,
                    "Orchid": 0.013374485596707819,
                    "PaleGoldenRod": 0.000257201646090535,
                    "PaleGreen": 0.0,
                    "PaleTurquoise": 0.01131687242798354,
                    "PaleVioletRed": 0.18415637860082304,
                    "PapayaWhip": 0.09156378600823045,
                    "PeachPuff": 0.005401234567901235,
                    "Peru": 0.0,
                    "Pink": 0.05581275720164609,
                    "Plum": 0.048868312757201646,
                    "PowderBlue": 0.009259259259259259,
                    "Purple": 0.00154320987654321,
                    "Red": 0.0,
                    "RosyBrown": 0.020061728395061727,
                    "RoyalBlue": 2.1790123456790123,
                    "SaddleBrown": 0.0,
                    "Salmon": 0.00154320987654321,
                    "SandyBrown": 0.0,
                    "SeaGreen": 0.0,
                    "SeaShell": 0.051183127572016464,
                    "Sienna": 0.00051440329218107,
                    "Silver": 0.14454732510288065,
                    "SkyBlue": 0.058127572016460904,
                    "SlateBlue": 9.415637860082304,
                    "SlateGray": 0.15715020576131689,
                    "Snow": 3.9068930041152266,
                    "SpringGreen": 0.0,
                    "SteelBlue": 1.2111625514403292,
                    "Tan": 0.001286008230452675,
                    "Teal": 0.000257201646090535,
                    "Thistle": 0.021347736625514403,
                    "Tomato": 0.0,
                    "Turquoise": 0.00051440329218107,
                    "Violet": 0.00205761316872428,
                    "Wheat": 0.001286008230452675,
                    "White": 32.8804012345679,
                    "WhiteSmoke": 1.425411522633745,
                    "Yellow": 0.0,
                    "YellowGreen": 0.0,
                },
                140,
            ),
        ),
    )
    def test_get_colors_w3c(self, image, expected_results, n_colors):
        output = get_colors_w3c(image, n_colors=n_colors)
        assert all(not isinstance(v, np.floating) for v in output.color_scheme.values())

        actual_results = output.color_scheme
        assert actual_results == expected_results

        assert output.image is None

    def test_exception(self, image, invalid_n_colors: int = 1):
        with pytest.raises(ValueError):
            get_colors_w3c(image, n_colors=invalid_n_colors)

    @pytest.mark.parametrize(argnames="is_plot", argvalues=(True, False))
    def test_plot(self, image, is_plot: bool):
        output = get_colors_w3c(image, n_colors=16, is_plot=is_plot)

        if is_plot:
            assert output.image is not None and isinstance(output.image, PilImage)
        else:
            assert output.image is None
