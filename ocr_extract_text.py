import pytesseract
import os
from PIL import Image
import glob

# Set Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

output_file = "primetime_manual.txt"
print("Starting OCR for all page-xxxx.png files...")

pages_processed = 0
empty_pages = 0

# Get all matching files in correct order
image_files = sorted(glob.glob("page-*.png"))

with open(output_file, "w", encoding="utf-8") as out:
    for filename in image_files:
        print(f"OCR on {filename}...")
        try:
            text = pytesseract.image_to_string(Image.open(filename), config="--psm 6 -l eng")
            if text.strip():
                out.write(f"\n--- {filename} ---\n{text}\n")
            else:
                empty_pages += 1
            pages_processed += 1
        except Exception as e:
            print(f"Error on {filename}: {e}")

print(f"Done. Pages processed: {pages_processed}. Empty pages: {empty_pages}. Output saved to {output_file}")
