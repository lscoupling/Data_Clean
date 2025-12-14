import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.parser import parse_questions


def print_parsed(parsed):
    print("--- parsed start ---")
    for q in parsed:
        print(q["id"])
        print("Q:", q["question"])
        print("Choices:")
        for k, v in q["choices"].items():
            print(f"  {k}: {v}")
        print("Answer:", q["answer"])
        print()
    print("--- parsed end ---")


def test_parse_basic_question_and_topic():
    text = """
Topic 1
Question #1
This is a sample question that spans
multiple lines to test collection.
A. First choice Most Voted
B. Second choice
C. Third choice
Correct Answer: B
"""
    parsed = parse_questions(text)
    assert len(parsed) == 1
    q = parsed[0]
    assert q["id"] == "Topic 1 Question #1"
    assert "sample question" in q["question"]
    assert q["choices"]["A"] == "First choice"
    assert q["choices"]["B"] == "Second choice"
    assert q["answer"] == "B"

    if os.getenv("DEBUG_PARSER"):
        print_parsed(parsed)


def test_parse_questions_from_data_pdfs():
    import glob
    import io
    import os
    import sys

    # Ensure pipeline is importable
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.pipeline import run_pipeline

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    pdf_paths = glob.glob(os.path.join(data_dir, "*.pdf"))

    assert pdf_paths, "No PDF files found in data/ to run integration test"

    for p in pdf_paths:
        with open(p, "rb") as f:
            pdf_bytes = io.BytesIO(f.read())

        questions = run_pipeline(pdf_bytes, format_output=False)  # 使用原始格式進行測試
        assert isinstance(questions, list)
        assert questions, f"No questions parsed from {p}"

        # Basic structure checks and print out for manual inspection
        for q in questions:
            assert "id" in q and q["id"], "Missing id"
            assert "question" in q, "Missing question"
            assert "choices" in q and isinstance(q["choices"], dict), "Missing or invalid choices"
            assert "answer" in q, "Missing answer field"

        if os.getenv("DEBUG_PARSER"):
            print(f"\n--- Parsed from {os.path.basename(p)} ---")
            print_parsed(questions)


def test_parse_real_pdf_expected_content():
    """Run pipeline on PDF files and assert we can find a real question by keywords
    and that its parsed answer and choices make sense.
    """
    import glob
    import io
    import os
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.pipeline import run_pipeline

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    pdf_paths = glob.glob(os.path.join(data_dir, "*.pdf"))
    assert pdf_paths, "No PDF files found in data/ to run integration test"

    found_target = False
    for p in pdf_paths:
        # focus on AWS sample file if present
        if "AWS" not in os.path.basename(p) and any("AWS" in os.path.basename(x) for x in pdf_paths):
            continue

        with open(p, "rb") as f:
            pdf_bytes = io.BytesIO(f.read())

        questions = run_pipeline(pdf_bytes, format_output=False)  # 使用原始格式

        # try to find a question mentioning AWS Glue and S3
        for q in questions:
            qtext = q.get("question", "")
            if "AWS Glue" in qtext or "Amazon S3" in qtext or "S3" in qtext:
                found_target = True
                # basic sanity checks
                assert q.get("answer"), "Expected an answer for AWS question"
                assert q["answer"] in q["choices"], "Answer must be one of the choices"
                # expect route-table / VPC gateway endpoint wording in choices or question
                combined = qtext + " " + " ".join(q["choices"].values())
                assert "route" in combined.lower() or "vpc" in combined.lower() or "s3" in combined.lower()
                break

        if found_target:
            break

    assert found_target, "Could not find an AWS-related question in data PDFs"


def test_parse_missing_topic_and_multiline_choice():
    """Integration test: find a real PDF that contains a multi-line choice
    (an option line followed by a continuation line that does not start with A.-F.)
    and assert the parser merges the continuation into the same choice value.
    """
    import glob
    import io
    import os
    import re
    import sys

    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
    from src.pdf_reader import read_pdf
    from src.pipeline import run_pipeline

    data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data"))
    pdf_paths = glob.glob(os.path.join(data_dir, "*.pdf"))
    if not pdf_paths:
        import pytest

        pytest.skip("No PDF files found in data/")

    multiline_found = False

    for p in pdf_paths:
        with open(p, "rb") as f:
            file_bytes = f.read()

        # build fresh streams so read_pdf and run_pipeline don't consume the same IO
        raw = read_pdf(io.BytesIO(file_bytes))

        # look for lines like "B. Option part1" followed by a continuation line
        m = re.search(r"(?m)^([A-F])\.\s+(.*)\n(?![A-F]\.\s+|Correct Answer|Question|Topic)(.+)", raw)
        if not m:
            continue

        multiline_found = True
        label = m.group(1)
        first = m.group(2).strip()
        cont = m.group(3).strip()

        questions = run_pipeline(io.BytesIO(file_bytes), format_output=False)  # 使用原始格式

        # find a parsed question that has this label and includes the continuation text
        matched = False
        cont_words = [w.strip(".,'\"()") for w in cont.split() if len(w) > 3]
        for q in questions:
            choice_val = q.get("choices", {}).get(label)
            if not choice_val:
                continue
            # check if any significant word from continuation appears in parsed choice
            if any(w in choice_val for w in cont_words):
                matched = True
                break

        assert matched, f"Multiline choice not merged correctly in {os.path.basename(p)}"

    import pytest
    if not multiline_found:
        pytest.skip("No multiline choices found in any data PDFs to validate parser behavior")


def test_parse_ignores_after_correct_answer():
    text = """
Topic 3
Question #5
Short Q
A. a
B. b
Correct Answer: A
Some trailing noise that should be ignored
Question #6
Question text
A. x
Correct Answer: A
"""
    parsed = parse_questions(text)
    assert len(parsed) == 2
    assert parsed[0]["answer"] == "A"
    assert "trailing noise" not in parsed[0]["question"].lower()

    if os.getenv("DEBUG_PARSER"):
        print_parsed(parsed)
