# pipeline.py - PDF 資料清洗流程協調器
from src.pdf_reader import read_pdf
from src.cleaner import clean_text
from src.parser import parse_questions
from src.formatter import format_questions_to_rows


def run_pipeline(pdf_bytes, verbose: bool = False, format_output: bool = True):
    """執行完整的 PDF 處理流程：讀取 → 清洗 → 解析 → 格式化
    
    Args:
        pdf_bytes: PDF 檔案的二進位流（io.BytesIO）
        verbose: 是否顯示清洗過程的詳細資訊
        format_output: 是否將結果轉換為扁平化格式（預設 True）
    
    Returns:
        list[dict]: 處理後的題目列表
            - 若 format_output=True：扁平化格式 (Topic, question_id, A~F, answer)
            - 若 format_output=False：原始格式 (id, question, choices, answer)
    """
    # 步驟 1: 從 PDF 提取原始文字
    raw_text = read_pdf(pdf_bytes)
    
    # 步驟 2: 清洗文字（移除雜訊、標準化空白等）
    cleaned_text = clean_text(raw_text, verbose=verbose)
    
    # 步驟 3: 解析成結構化的題目資料
    questions = parse_questions(cleaned_text)
    
    # 步驟 4: 轉換為扁平化格式（可選）
    if format_output:
        return format_questions_to_rows(questions)
    
    return questions
