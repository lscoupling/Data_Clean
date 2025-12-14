import io
import os
import sys
import fitz

# Ensure the package `src` is importable when running tests
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.pdf_reader import read_pdf


def make_pdf_bytes(text: str) -> io.BytesIO:
    doc = fitz.open()
    page = doc.new_page()
    page.insert_text((72, 72), text)
    pdf_bytes = io.BytesIO(doc.write())
    return pdf_bytes


def test_read_pdf_extracts_text():
    import os

    sample = "Hello from test PDF"
    pdf_bytes = make_pdf_bytes(sample)

    extracted = read_pdf(pdf_bytes)

    assert sample in extracted

    # Always print extraction & cleaning during tests
    from src.cleaner import clean_text_with_stats
    cleaned, stats = clean_text_with_stats(extracted, verbose=True)

    # Optional debug print: set DEBUG_PDF_TEST=1 to see full extracted text
    if os.getenv("DEBUG_PDF_TEST"):
        print('\n--- extracted (first 500 chars) ---\n')
        print(extracted[:500])
        print('\n--- end ---\n')


def test_read_pdf_from_data_dir():
    import glob
    import os
    import io
    import pytest

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    pdf_paths = glob.glob(os.path.join(data_dir, "*.pdf"))

    if not pdf_paths:
        pytest.skip("No PDF files found in data/ to test against")

    for p in pdf_paths:
        with open(p, "rb") as f:
            pdf_bytes = io.BytesIO(f.read())

        extracted = read_pdf(pdf_bytes)
        assert extracted and extracted.strip(), f"No text extracted from {p}"

        # Always print cleaning stats during tests
        from src.cleaner import clean_text_with_stats
        cleaned, stats = clean_text_with_stats(extracted, verbose=True)

        if os.getenv("DEBUG_PDF_TEST"):
            print(f"\n--- {os.path.basename(p)} (first 500 chars) ---\n")
            print(extracted[:500])
            print('\n--- end ---\n')
