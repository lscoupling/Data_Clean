#!/usr/bin/env python
# example_with_formatter.py - 示範如何使用 formatter 轉換並輸出資料
r"""
使用範例：
  python examples/example_with_formatter.py "data/AWS  P1-P3.pdf"
"""
import sys
import io
import os

# 將 pdf-cleaning 加入路徑
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "pdf-cleaning")))

from src.pipeline import run_pipeline
from src.formatter import format_questions_to_rows


def main():
    if len(sys.argv) != 2:
        print("用法：python examples/example_with_formatter.py <pdf_path>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    # 讀取 PDF
    with open(pdf_path, "rb") as f:
        pdf_bytes = io.BytesIO(f.read())

    # 執行完整流程：讀取 → 清洗 → 解析（使用原始格式）
    questions = run_pipeline(pdf_bytes, verbose=False, format_output=False)

    # 轉換為扁平化格式
    rows = format_questions_to_rows(questions)

    # 輸出結果（以表格形式顯示前 3 題）
    print(f"\n共解析出 {len(rows)} 題\n")
    print("=" * 80)
    
    for i, row in enumerate(rows[:3], 1):
        print(f"題目 {i}: Topic {row['Topic']} Q#{row['question_id']}")
        print(f"問題: {row['question'][:80]}...")
        print(f"選項:")
        for opt in ['A', 'B', 'C', 'D']:
            if row[opt]:
                print(f"  {opt}. {row[opt][:60]}...")
        print(f"答案: {row['answer']}")
        print("-" * 80)

    # 若需要輸出為 CSV，可取消下面註解
    # import csv
    # with open("output.csv", "w", encoding="utf-8", newline="") as f:
    #     writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    #     writer.writeheader()
    #     writer.writerows(rows)
    # print("\n已輸出至 output.csv")


if __name__ == "__main__":
    main()
