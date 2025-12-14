# formatter.py - 資料格式轉換模組：將解析結果轉換為扁平化欄位格式
import re


def format_questions_to_rows(questions: list) -> list:
    """將解析後的題目列表轉換為扁平化的資料列格式
    
    將原始的 {id, question, choices, answer} 格式轉換為：
    {Topic, question_id, question, A, B, C, D, E, F, answer}
    
    Args:
        questions: parse_questions() 回傳的題目列表
    
    Returns:
        list[dict]: 轉換後的資料列，每列包含：
            - Topic: 主題編號（數字或 "NaN"）
            - question_id: 題目編號
            - question: 題目文字
            - A, B, C, D, E, F: 各選項內容（不存在時為空字串）
            - answer: 正確答案
    """
    final_rows = []

    for q in questions:
        # 從 id 欄位解析出 Topic 與 Question 編號
        # 例如: "Topic 1 Question #1" 或 "Topic NaN Question #2"
        m = re.match(r"^Topic\s+(\d+|NaN)\s+Question #(\d+)", q["id"])

        if not m:
            # 若無法解析 id 格式，跳過此題
            continue

        topic = m.group(1)        # Topic 編號（數字或 "NaN"）
        qid = m.group(2)          # Question 編號

        # 提取各選項（若不存在則補空字串）
        A = q["choices"].get("A", "")
        B = q["choices"].get("B", "")
        C = q["choices"].get("C", "")
        D = q["choices"].get("D", "")
        E = q["choices"].get("E", "")
        F = q["choices"].get("F", "")

        # 組裝成新的扁平化資料列
        final_rows.append({
            "Topic": topic,
            "question_id": qid,
            "question": q["question"],
            "A": A,
            "B": B,
            "C": C,
            "D": D,
            "E": E,
            "F": F,
            "answer": q["answer"]
        })

    return final_rows
