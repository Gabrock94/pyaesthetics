import abc
from typing import Optional

from PIL.Image import Image as PilImage


class TextDetector(object, metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def __call__(self, image: PilImage, *args, **kwargs) -> str:
        raise NotImplementedError


class TesseractTextDetector(TextDetector):
    def __call__(self, image: PilImage, *args, **kwargs) -> str:
        import pytesseract

        text = pytesseract.image_to_string(image)
        return text


def detect_text(image: PilImage, text_detector: Optional[TextDetector] = None) -> int:
    text_detector = text_detector or TesseractTextDetector()
    return len(text_detector(image))
