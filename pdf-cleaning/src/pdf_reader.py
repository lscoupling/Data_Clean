# pdf_reader.py - PDF 讀取模組：從 PDF 檔案中提取原始文字
import fitz  # PyMuPDF 套件
import io

def read_pdf(pdf_bytes: io.BytesIO) -> str:
    """從 PDF 二進位流中提取所有頁面的文字內容
    
    Args:
        pdf_bytes: PDF 檔案的二進位流 (io.BytesIO)
    
    Returns:
        str: 提取出的原始文字內容（包含所有頁面）
    """
    # 使用 PyMuPDF (fitz) 開啟 PDF 文件
    doc = fitz.open(stream=pdf_bytes.read(), filetype="pdf")

    raw_text = ""
    # 逐頁提取文字
    for page in doc:
        text = page.get_text()
        if text:
            raw_text += text + "\n"

    return raw_text
