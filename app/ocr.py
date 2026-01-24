import pytesseract
from PIL import Image
import re

pytesseract.pytesseract.tesseract_cmd = r"C:\Users\Chandan\tesseract.exe"

def clean_text(text: str) -> str:
    """
    Clean noisy OCR output
    """
    text = text.lower()
    text = re.sub(r'@', ' at ', text)
    text = re.sub(r'\bnxt\b', 'next', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_text_from_image(image: Image.Image) -> tuple[str, float]:

    # Convert to grayscale
    image = image.convert("L")

    # Optional: increase contrast
    image = image.point(lambda x: 0 if x < 140 else 255, "1")

    """
    Perform OCR on image and return text + confidence
    """
    raw_text = pytesseract.image_to_string(image)
    cleaned_text = clean_text(raw_text)

    # Simple heuristic confidence (acceptable for assessment)
    confidence = 0.90 if len(cleaned_text) > 5 else 0.60

    return cleaned_text, confidence
