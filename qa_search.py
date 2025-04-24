import re
import csv

# Load OCR'd manual
with open("primetime_manual.txt", encoding="utf-8") as f:
    content = f.read()

paragraphs = re.split(r'\n\s*\n', content)

query = input("Enter a keyword or phrase to search: ").strip()
query_lower = query.lower()

results = []

for para in paragraphs:
    if query_lower in para.lower():
        results.append(para.strip())
    if len(results) == 10:
        break

def extract_page_and_clean(text):
    # Extract page ref if present
    page_match = re.match(r'^--- (page-\d+\.png) ---\s*(.*)', text, re.DOTALL)
    if page_match:
        page = page_match.group(1)
        body = page_match.group(2)
    else:
        page = "Unknown"
        body = text
    # Collapse newlines & remove artifacts
    cleaned = re.sub(r'\s+', ' ', body)
    return page, cleaned

if results:
    print(f"\nFound {len(results)} result(s) for '{query}':\n")

    with open("search_results.txt", "w", encoding="utf-8") as txt_file, \
         open("search_results.csv", "w", newline="", encoding="utf-8") as csv_file:

        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Result Number", "Source Page", "Paragraph"])

        for i, res in enumerate(results, 1):
            # For display with highlight
            highlight = re.sub(re.escape(query), f"[{query}]", res, flags=re.IGNORECASE)

            # For export cleaned
            page, clean_export = extract_page_and_clean(res)

            print(f"\nResult {i}:\n{highlight}\n")

            txt_file.write(f"\nResult {i} (from {page}):\n{highlight}\n")
            csv_writer.writerow([i, page, clean_export])

    print("Results saved to 'search_results.txt' and 'search_results.csv'.")
else:
    print("No results found.")
