import pytesseract
from PIL.Image import Image as PilImage


def detect_text(img: PilImage) -> int:
    text = pytesseract.image_to_string(img)
    return len(text)
