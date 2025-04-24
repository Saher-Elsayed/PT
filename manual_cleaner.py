import re
from pathlib import Path

# === CONFIG ===
INPUT_FILE = "primetime_manual.txt"
OUTPUT_FILE = "primetime_cleaned_final_strict.txt"

# === LOAD RAW OCR FILE ===
raw_path = Path(INPUT_FILE)
raw_text = raw_path.read_text(encoding="utf-8")

# === STEP 1: Split into page blocks ===
page_blocks = re.split(r"\n\s*---\s*(page-\d+\.png)\s*---\s*\n", raw_text)
page_data = list(zip(page_blocks[1::2], page_blocks[2::2]))  # (page, text) tuples

# === STEP 2: Function to clean individual page content ===
def clean_page_text(text):
    # Remove junk patterns
    text = re.sub(r"(e{3,}|c{3,}|0{4,}|\.{5,})", " ", text)

    # Normalize whitespace
    text = re.sub(r"\s+", " ", text)

    # Re-split into readable lines
    text = re.sub(r"(?<=[a-zA-Z0-9])\s*\.\s*", ".\n", text)

    # Fix bullet formatting
    text = re.sub(r"\*\s*", "\n- ", text)
    text = re.sub(r"\+\s*", "\n- ", text)

    # Capitalize chapter headings
    text = re.sub(r"(chapter\s+\d+)", lambda m: m.group(1).title(), text, flags=re.IGNORECASE)

    return text.strip()

# === STEP 3: Clean all pages ===
cleaned_pages = []
for page, content in page_data:
    cleaned = clean_page_text(content)
    cleaned_pages.append(f"--- {page} ---\n{cleaned}")

# === STEP 4: Remove Disclaimers and Branding from Full Text ===
full_text = "\n\n".join(cleaned_pages)

# Remove version marks, dates, copyrights, trademarks, feedback
patterns_to_remove = [
    r"PrimeTime®\s+User\s+Guide",
    r"Version:\s*V-\d{4,}",
    r"\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\b\s+\d{4}",
    r"©?\s?\d{4}\s+Synopsys.*?(?=\n)",
    r"Synopsys®?",
    r"All rights reserved.*",
    r"Feedback.*?(?=\n)",
]
for pattern in patterns_to_remove:
    full_text = re.sub(pattern, "", full_text, flags=re.IGNORECASE)

# Final cleanup of extra newlines
full_text = re.sub(r"\n\s*\n\s*\n+", "\n\n", full_text)

# === STEP 5: Save to Output File ===
Path(OUTPUT_FILE).write_text(full_text.strip(), encoding="utf-8")
print(f"✅ Cleaned manual saved as: {OUTPUT_FILE}")
