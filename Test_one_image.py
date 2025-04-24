from PIL import Image
import pytesseract

# Point to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Load and OCR one real image
img = Image.open("page-1330.png")
text = pytesseract.image_to_string(img, config="--psm 6 -l eng")

print(text if text.strip() else "No text found.")
