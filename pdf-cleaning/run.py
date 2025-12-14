# run.py - 命令列執行腳本：啟動 PDF 清洗流程的入口程式
import sys
import io
import argparse
from src.pipeline import run_pipeline


def main():
    """命令列介面主程式
    
    使用方式：
        python run.py <pdf_path>              # 基本使用
        python run.py <pdf_path> --verbose    # 顯示清洗過程細節
    """
    # 設定命令列參數解析器
    parser = argparse.ArgumentParser(description="執行 PDF 資料清洗流程")
    parser.add_argument("pdf_path", help="PDF 檔案路徑")
    parser.add_argument("--verbose", action="store_true", help="顯示詳細的清洗過程資訊")
    parser.add_argument("--raw", action="store_true", help="輸出原始格式（不進行扁平化轉換）")
    args = parser.parse_args()

    # 讀取 PDF 檔案並轉換為二進位流
    with open(args.pdf_path, "rb") as f:
        pdf_bytes = io.BytesIO(f.read())

    # 執行完整的處理流程（預設會格式化輸出）
    results = run_pipeline(pdf_bytes, verbose=args.verbose, format_output=not args.raw)

    # 輸出解析結果
    for item in results:
        print(item)


if __name__ == "__main__":
    main()
