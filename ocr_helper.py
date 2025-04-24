import pytesseract
import os
from PIL import Image

print("🛠 Step 1: Using Poppler manually to convert PDF to PNG images...")
os.system("pdftoppm img20240506115606.pdf page -png")

print("🧠 Step 2: Starting OCR on images...")

output_file = "primetime_manual.txt"
with open(output_file, "w", encoding="utf-8") as out:
    page_num = 1
    while True:
        img_path = f"page-{page_num}.png"
        if not os.path.exists(img_path):
            break
        print(f"🔍 OCR processing {img_path}")
        text = pytesseract.image_to_string(Image.open(img_path))
        out.write(f"\n--- PAGE {page_num} ---\n{text}")
        page_num += 1

print(f"✅ OCR complete! Text saved to: {output_file}")
