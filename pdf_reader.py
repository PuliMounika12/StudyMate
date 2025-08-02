import fitz  # PyMuPDF
import pytesseract
from pdf2image import convert_from_path
import os

# Optional: set this to your Tesseract install path if needed
# pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def extract_text_from_pdf(file_path):
    doc = fitz.open(file_path)
    text = ""
    for page in doc:
        text += page.get_text()

    if len(text.strip()) < 50:  # Try OCR if not enough text
        print("⚠️ Low text detected — using OCR")
        text = extract_text_with_ocr(file_path)

    print("🧾 Extracted text length:", len(text))
    return text

def extract_text_with_ocr(file_path):
    images = convert_from_path(file_path)
    full_text = ""
    for i, image in enumerate(images):
        text = pytesseract.image_to_string(image)
        full_text += f"\n--- Page {i+1} ---\n{text}"
    return full_text
