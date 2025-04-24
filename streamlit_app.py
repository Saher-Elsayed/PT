import streamlit as st
import re
from pathlib import Path

st.set_page_config(page_title="PrimeTime Sentence Search", layout="wide")

# Load cleaned manual
@st.cache_data
def load_manual():
    with open("primetime_cleaned_final.txt", "r", encoding="utf-8") as f:
        text = f.read()
    parts = re.split(r"\n---\s*(page-\d+\.png)\s*---\n", text)
    return list(zip(parts[1::2], parts[2::2]))  # [(page, text)]

pages = load_manual()

# Styling
st.markdown("""
<style>
.result-box {
    background-color: #1e1e1e;
    border-radius: 10px;
    padding: 16px;
    border: 1px solid #444;
    margin-bottom: 20px;
    color: #f0f0f0;
}
.match-sentence {
    font-size: 16px;
    line-height: 1.6;
    margin-bottom: 10px;
}
.page-label {
    font-size: 14px;
    color: #aaa;
}
</style>
""", unsafe_allow_html=True)

st.markdown("## 🔍 PrimeTime Sentence Search")
query = st.text_input("Enter a keyword or phrase:")

if query:
    pattern = re.compile(rf"\b{re.escape(query)}\b", re.IGNORECASE)
    results = []

    for page, text in pages:
        sentences = re.split(r'(?<=[.?!])\s+', text)
        for sent in sentences:
            if pattern.search(sent):
                highlighted = pattern.sub(lambda m: f"<span style='background-color:#fffa8b;font-weight:bold'>{m.group(0)}</span>", sent)
                results.append((highlighted, page))
                break  # only one match per page

    if results:
        st.success(f"Showing {len(results)} results (one per page) for **'{query}'**")

        for i, (sentence, page) in enumerate(results, 1):
            st.markdown(f"<div class='result-box'>", unsafe_allow_html=True)
            st.markdown(f"<div class='match-sentence'>{i}. {sentence}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='page-label'>Page: {page}</div>", unsafe_allow_html=True)

            image_path = Path(page)
            if image_path.exists():
                st.image(str(image_path), use_column_width=True)
            else:
                st.warning(f"⚠️ Image not found: {page}")
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.warning("No matches found.")
