import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.formatter import format_questions_to_rows


def test_format_questions_to_rows():
    """測試題目格式轉換功能"""
    # 模擬 parse_questions 的輸出
    questions = [
        {
            "id": "Topic 1 Question #1",
            "question": "Sample question text",
            "choices": {
                "A": "Option A",
                "B": "Option B",
                "C": "Option C",
                "D": "Option D"
            },
            "answer": "B"
        },
        {
            "id": "Topic NaN Question #2",
            "question": "Another question",
            "choices": {
                "A": "Choice A",
                "B": "Choice B",
                "C": "Choice C"
            },
            "answer": "A"
        }
    ]

    rows = format_questions_to_rows(questions)

    # 驗證轉換結果
    assert len(rows) == 2

    # 檢查第一題
    assert rows[0]["Topic"] == "1"
    assert rows[0]["question_id"] == "1"
    assert rows[0]["question"] == "Sample question text"
    assert rows[0]["A"] == "Option A"
    assert rows[0]["B"] == "Option B"
    assert rows[0]["D"] == "Option D"
    assert rows[0]["E"] == ""  # 不存在的選項應為空字串
    assert rows[0]["F"] == ""
    assert rows[0]["answer"] == "B"

    # 檢查第二題（Topic NaN）
    assert rows[1]["Topic"] == "NaN"
    assert rows[1]["question_id"] == "2"
    assert rows[1]["D"] == ""  # 此題沒有 D 選項
    assert rows[1]["answer"] == "A"


def test_format_with_real_pipeline():
    """整合測試：從 data PDF 執行完整流程並轉換格式"""
    import glob
    import io
    from src.pipeline import run_pipeline

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    pdf_paths = glob.glob(os.path.join(data_dir, "*.pdf"))

    if not pdf_paths:
        import pytest
        pytest.skip("No PDF files found in data/")

    # 取第一個 PDF 測試
    with open(pdf_paths[0], "rb") as f:
        pdf_bytes = io.BytesIO(f.read())

    questions = run_pipeline(pdf_bytes)
    rows = format_questions_to_rows(questions)

    # 驗證基本結構
    assert isinstance(rows, list)
    assert rows, "Should have at least one formatted row"

    for row in rows:
        assert "Topic" in row
        assert "question_id" in row
        assert "question" in row
        assert "A" in row
        assert "answer" in row
        # 確保欄位都是字串（非 None）
        assert isinstance(row["A"], str)
        assert isinstance(row["answer"], str)
