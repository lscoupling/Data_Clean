# PDF 資料清洗專案

專門用於清洗、解析和結構化 PDF 考題資料的 Python 工具。

## 📋 專案簡介

本專案提供完整的 PDF 資料處理管線,能夠：
- 從 PDF 檔案中提取文字內容
- 清理文字雜訊（如廣告、特殊字符）
- 解析考題結構（題目、選項、答案）
- 轉換為標準化的扁平格式

## 🏗️ 專案結構

```
Data_Clean/
├── pdf-cleaning/              # 主要程式碼目錄
│   ├── src/                   # 核心模組
│   │   ├── pdf_reader.py      # PDF 讀取模組
│   │   ├── cleaner.py         # 文字清理模組
│   │   ├── parser.py          # 考題解析模組
│   │   ├── formatter.py       # 格式轉換模組
│   │   └── pipeline.py        # 處理管線
│   ├── tests/                 # 單元測試
│   │   ├── test_pdf_reader.py
│   │   ├── test_cleaner.py
│   │   ├── test_parser.py
│   │   └── test_formatter.py
│   ├── requirements.txt       # 生產環境依賴
│   ├── requirements-dev.txt   # 開發環境依賴
│   └── run.py                 # CLI 入口程式
├── examples/                  # 使用範例
│   ├── quick_start.py
│   └── example_with_formatter.py
├── data/                      # 測試資料
│   └── AWS  P1-P3.pdf
└── pytest.ini                 # pytest 設定檔
```

## 🚀 安裝

### 基本需求

- Python 3.12+
- pip

### 安裝步驟

1. **克隆專案**
   ```bash
   git clone https://github.com/lscoupling/Data_Clean.git
   cd Data_Clean
   ```

2. **安裝依賴**
   ```bash
   # 生產環境
   pip install -r pdf-cleaning/requirements.txt
   
   # 開發環境（包含測試工具）
   pip install -r pdf-cleaning/requirements-dev.txt
   ```

### 主要依賴套件

- **PyMuPDF (fitz)** >= 1.23.0 - PDF 文字提取
- **pandas** >= 2.0.0 - 資料處理


## 💻 使用方式

### 命令列介面 (CLI)

```bash
# 基本使用（輸出扁平化格式）
python pdf-cleaning/run.py "data/AWS  P1-P3.pdf"

# 輸出原始格式
python pdf-cleaning/run.py "data/AWS  P1-P3.pdf" --raw

# 顯示詳細處理過程
python pdf-cleaning/run.py "data/AWS  P1-P3.pdf" --verbose

# 結合選項
python pdf-cleaning/run.py "data/AWS  P1-P3.pdf" --verbose --raw
```

### Python API

```python
from pdf_cleaning.src.pipeline import run_pipeline
import io

# 讀取 PDF 檔案
with open("data/AWS  P1-P3.pdf", "rb") as f:
    pdf_bytes = io.BytesIO(f.read())

# 使用預設扁平化格式
formatted_results = run_pipeline(pdf_bytes, format_output=True)
# 輸出: [
#   {
#     'Topic': '1',
#     'question_id': '1',
#     'question': '題目內容...',
#     'A': '選項 A',
#     'B': '選項 B',
#     'C': '選項 C',
#     'D': '選項 D',
#     'E': '',  # 選項不存在時為空字串
#     'F': '',
#     'answer': 'D'
#   },
#   ...
# ]

# 使用原始格式
raw_results = run_pipeline(pdf_bytes, format_output=False)
# 輸出: [
#   {
#     'id': 'Topic 1 Question #1',
#     'question': '題目內容...',
#     'choices': {
#       'A': '選項 A',
#       'B': '選項 B',
#       'C': '選項 C',
#       'D': '選項 D'
#     },
#     'answer': 'D'
#   },
#   ...
# ]

# 啟用詳細輸出（顯示清理統計資訊）
results = run_pipeline(pdf_bytes, verbose=True, format_output=True)
```

### 個別模組使用

```python
from pdf_cleaning.src.pdf_reader import read_pdf
from pdf_cleaning.src.cleaner import clean_text_with_stats
from pdf_cleaning.src.parser import parse_questions
from pdf_cleaning.src.formatter import format_questions_to_rows

# 步驟 1: 讀取 PDF
raw_text = read_pdf(pdf_bytes)

# 步驟 2: 清理文字
cleaned_text, stats = clean_text_with_stats(raw_text, verbose=True)
print(f"清理次數: {stats['weixin_removed']}，替換次數: {stats['nbsp_replaced']}")

# 步驟 3: 解析問題
questions = parse_questions(cleaned_text)

# 步驟 4: 格式化輸出
formatted_rows = format_questions_to_rows(questions)
```

## 🔧 功能模組

### 1. PDF 讀取器 (`pdf_reader.py`)

- **功能**: 使用 PyMuPDF 提取 PDF 文字
- **輸入**: PDF 二進制資料 (`io.BytesIO`)
- **輸出**: 原始文字字串

### 2. 文字清理器 (`cleaner.py`)

- **功能**: 
  - 移除廣告文字（如「店长微信：xxx」）
  - 替換特殊字符（`\xa0` → 空格）
  - 統計清理次數
- **輸入**: 原始文字
- **輸出**: 清理後文字 + 統計資訊

### 3. 考題解析器 (`parser.py`)

- **功能**:
  - 識別主題 (Topic)
  - 解析問題編號
  - 提取問題內容
  - 解析選項（A-F）
  - 識別正確答案
  - 處理多行選項
  - 移除「Most Voted」標記
- **輸入**: 清理後文字
- **輸出**: 結構化問題列表

### 4. 格式轉換器 (`formatter.py`)

- **功能**: 
  - 將巢狀結構轉換為扁平格式
  - 補齊缺失的選項欄位（E、F）
  - 適合匯出為 CSV/Excel
- **輸入**: 解析後的問題列表
- **輸出**: 扁平化資料列表

### 5. 處理管線 (`pipeline.py`)

- **功能**: 整合所有模組，提供一站式處理
- **參數**:
  - `pdf_bytes`: PDF 二進制資料
  - `verbose`: 是否顯示詳細過程（預設 `False`）
  - `format_output`: 是否格式化輸出（預設 `True`）

## 🧪 測試

### 執行所有測試

```bash
# 基本測試
pytest pdf-cleaning/tests/

# 顯示詳細輸出
pytest pdf-cleaning/tests/ -v

# 顯示測試覆蓋率
pytest pdf-cleaning/tests/ --cov=pdf-cleaning/src
```

### 測試結構

- **test_pdf_reader.py**: 測試 PDF 讀取功能
  - 基本文字提取
  - 真實 PDF 檔案處理
  - 空白 PDF 處理

- **test_cleaner.py**: 測試文字清理功能
  - 廣告移除
  - 特殊字符替換
  - 統計資訊準確性

- **test_parser.py**: 測試考題解析功能
  - 問題結構解析
  - 多行選項處理
  - 真實 PDF 整合測試

- **test_formatter.py**: 測試格式轉換功能
  - 扁平化轉換
  - 缺失選項處理

### 測試設定

`pytest.ini` 設定為顯示標準輸出（`-s`），方便除錯：
```ini
[tool:pytest]
addopts = -s
```

啟用除錯模式的環境變數：
```bash
# 啟用 PDF 讀取器除錯輸出
export DEBUG_PDF_TEST=1

# 啟用解析器除錯輸出
export DEBUG_PARSER=1

# 執行測試
pytest pdf-cleaning/tests/test_parser.py -v
```

## 📊 輸出格式

### 扁平化格式（預設）

適合匯出為 CSV 或 Excel：

```python
{
    'Topic': '1',
    'question_id': '1',
    'question': '完整的題目內容...',
    'A': '選項 A 內容',
    'B': '選項 B 內容',
    'C': '選項 C 內容',
    'D': '選項 D 內容',
    'E': '',  # 沒有選項 E 時為空字串
    'F': '',  # 沒有選項 F 時為空字串
    'answer': 'D'
}
```

### 原始格式（`--raw` 或 `format_output=False`）

保持巢狀結構：

```python
{
    'id': 'Topic 1 Question #1',
    'question': '完整的題目內容...',
    'choices': {
        'A': '選項 A 內容',
        'B': '選項 B 內容',
        'C': '選項 C 內容',
        'D': '選項 D 內容'
    },
    'answer': 'D'
}
```

## 📝 範例程式

### 範例 1: 快速開始 (`examples/quick_start.py`)

展示基本的 PDF 文字提取。

```bash
python examples/quick_start.py "data/AWS  P1-P3.pdf"
```

### 範例 2: 使用格式轉換器 (`examples/example_with_formatter.py`)

展示如何使用格式轉換器並匯出為 CSV。

```bash
python examples/example_with_formatter.py
```

## 🔍 除錯技巧

### 1. 查看清理統計

```bash
python pdf-cleaning/run.py "data/AWS  P1-P3.pdf" --verbose
```

輸出範例：
```
=== 清理統計 ===
移除微信廣告: 5 次
替換不間斷空格: 328 次
```

### 2. 檢查解析結果

```python
# 使用原始格式查看完整結構
results = run_pipeline(pdf_bytes, format_output=False)
for q in results[:3]:  # 查看前 3 題
    print(q)
```

### 3. 測試特定功能

```bash
# 只測試解析器
pytest pdf-cleaning/tests/test_parser.py -v

# 測試特定測試函數
pytest pdf-cleaning/tests/test_parser.py::test_parse_real_pdf_expected_content -v
```


### 新增功能流程



## ⚠️ 注意事項

1. **編碼**: 所有檔案使用 UTF-8 編碼
2. **PDF 格式**: 僅支援文字型 PDF，不支援掃描影像
3. **記憶體**: 大型 PDF 檔案會消耗較多記憶體
4. **格式限制**: 解析器針對特定考題格式設計，可能需要調整正則表達式

