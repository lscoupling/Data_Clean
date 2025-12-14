"""Quick start example for reading PDF bytes and extracting text.

Keep this minimal and portable (no Colab-specific code, no !pip lines).
"""
import re
import fitz
import io


def extract_text_from_file(path: str) -> str:
    with open(path, "rb") as f:
        pdf_bytes = io.BytesIO(f.read())

    doc = fitz.open(stream=pdf_bytes.read(), filetype="pdf")
    text = []
    for page in doc:
        t = page.get_text()
        if t:
            text.append(t)
    return "\n".join(text)


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python examples/quick_start.py <pdf_path>")
        raise SystemExit(1)

    print(extract_text_from_file(sys.argv[1]))
