# parser.py - 文字解析模組：將清洗後的文字解析成結構化題目
import re

def parse_questions(cleaned_text: str) -> list:
    """解析清洗後的文字，提取題目、選項與答案
    
    Args:
        cleaned_text: 已清洗的文字內容
    
    Returns:
        list[dict]: 題目列表，每題包含：
            - id: 題目編號（如 "Topic 1 Question #1"）
            - question: 題目文字
            - choices: 選項字典 {'A': '選項內容', 'B': ...}
            - answer: 正確答案（如 'A'）
    """
    lines = cleaned_text.splitlines()

    questions = []  # 儲存所有解析出的題目
    current = None  # 目前正在處理的題目

    # 狀態變數
    collecting_question = False  # 是否正在收集題目文字
    collecting_choices = False   # 是否正在收集選項
    pending_topic = None         # 待處理的 Topic 編號
    last_key = None              # 最後一個選項的標籤（用於跨行合併）
    ignore_until_next_question = False  # 遇到 Correct Answer 後忽略後續內容

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # 偵測 Topic X（主題編號）
        t = re.match(r"^Topic\s*(\d+)", line)
        if t:
            pending_topic = f"Topic {t.group(1)}"
            continue

        # 偵測 Question #Y（題目編號）
        q = re.match(r"^Question\s*#\s*(\d+)", line)
        if q:
            if current:
                questions.append(current)

            if pending_topic is None:
                pending_topic = "Topic NaN"

            current = {
                "id": f"{pending_topic} Question #{q.group(1)}",
                "question": "",
                "choices": {},
                "answer": ""
            }

            pending_topic = None
            collecting_question = True
            collecting_choices = False
            ignore_until_next_question = False
            last_key = None
            continue

        if not current:
            continue

        # Correct Answer
        ans = re.match(r"^Correct Answer\s*:?\s*([A-F]+)", line)
        if ans:
            current["answer"] = ans.group(1)
            collecting_question = False
            collecting_choices = False
            ignore_until_next_question = True
            last_key = None
            continue

        # Correct Answer 後全部忽略
        if ignore_until_next_question:
            continue

        # 選項 A–F
        opt = re.match(r"^([A-F])\.\s+(.*)", line)
        if opt and collecting_question:
            clean_choice = re.sub(r"\s*Most Voted.*$", "", opt.group(2)).strip()
            last_key = opt.group(1)
            current["choices"][last_key] = clean_choice
            collecting_choices = True
            continue

        # 跨行選項
        if collecting_choices and last_key and not re.match(r"^[A-F]\.\s+", line):
            current["choices"][last_key] += " " + line
            continue

        # 跨行題目
        if collecting_question and not collecting_choices:
            current["question"] += line + " "
            continue

    if current:
        questions.append(current)

    return questions
