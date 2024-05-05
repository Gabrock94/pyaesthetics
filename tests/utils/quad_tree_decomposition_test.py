from PIL import Image

from pyaesthetics.utils import PyaestheticsTestCase, QuadTreeDecomposer


class TestQuadTreeDecomposition(PyaestheticsTestCase):
    def test_quad_tree(self, min_std: int = 15, min_size: int = 40):
        sample_image_path = str(self.FIXTURES_ROOT / "sample.jpg")
        img = Image.open(sample_image_path)

        quad_tree = QuadTreeDecomposer(img=img, min_std=min_std, min_size=min_size)

        assert len(quad_tree.decompose(x=0, y=0)) == 781
        assert len(quad_tree.blocks) == 781

        plot_img = quad_tree.get_plot()
        assert img.size == plot_img.size
