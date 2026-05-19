import re
from pathlib import Path


def test_retrieval_eval_dataset_has_required_coverage() -> None:
    doc = Path("docs/retrieval_eval.md").read_text()
    rows = [
        line for line in doc.splitlines() if re.match(r"\| Q\d{2} \|", line) is not None
    ]

    assert len(rows) >= 10
    joined = "\n".join(rows)
    assert "| simple |" in joined
    assert "| multi-doc |" in joined
    assert "| multi-hop |" in joined
    assert "| no-answer |" in joined
    assert "Customer Data section" in joined


def test_evaluation_history_rows_have_required_fields() -> None:
    doc = Path("docs/retrieval_eval.md").read_text()
    in_history = False
    rows = []
    for line in doc.splitlines():
        if line == "## Evaluation History":
            in_history = True
            continue
        if in_history and line.startswith("## "):
            break
        if in_history and re.match(r"\| 20\d{2}-\d{2}-\d{2} \|", line):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])

    assert rows
    for row in rows:
        assert row[0]
        assert row[2]
        assert row[3]
