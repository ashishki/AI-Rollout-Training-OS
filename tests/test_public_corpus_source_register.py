import json
from pathlib import Path

REGISTER_PATH = Path("docs/public_corpus/ai_rollout_source_register.md")
FIXTURE_PATH = Path("tests/fixtures/seed_training_documents.json")


def _source_rows() -> list[dict[str, str]]:
    lines = REGISTER_PATH.read_text().splitlines()
    header_index = lines.index(
        "| source_url_or_locator | captured_at | source_type | role_or_policy_use | "
        "extracted_fact | demo_use | limitation |"
    )
    rows = []
    for line in lines[header_index + 2 :]:
        if not line.startswith("| "):
            break
        cells = [cell.strip() for cell in line.strip("|").split("|")]
        rows.append(
            {
                "source_url_or_locator": cells[0],
                "captured_at": cells[1],
                "source_type": cells[2],
                "role_or_policy_use": cells[3],
                "extracted_fact": cells[4],
                "demo_use": cells[5],
                "limitation": cells[6],
            }
        )
    return rows


def test_public_source_register_has_required_sources_and_fields() -> None:
    rows = _source_rows()

    assert len(rows) >= 15
    for row in rows:
        assert row["source_url_or_locator"].startswith("https://")
        assert row["captured_at"] == "2026-05-23"
        assert row["source_type"]
        assert row["role_or_policy_use"]
        assert row["extracted_fact"]
        assert row["demo_use"]
        assert row["limitation"]


def test_public_source_register_blocks_private_data_and_overclaims() -> None:
    register = REGISTER_PATH.read_text()

    for phrase in [
        "public demo source register",
        "Public sources do not prove",
        "Do not copy large source text",
        "insufficient_evidence",
        "enterprise readiness",
        "productivity lift",
        "GA readiness",
    ]:
        assert phrase in register

    forbidden_private_markers = [
        "employee@example.com",
        "customer@example.com",
        "api_key",
        "password:",
        "private company policy",
    ]
    lowered = register.lower()
    for marker in forbidden_private_markers:
        assert marker not in lowered


def test_seed_fixture_indexes_public_sources_without_eval_corpus_change() -> None:
    fixture = json.loads(FIXTURE_PATH.read_text())

    assert fixture["corpus_version"] == "eval-corpus-v1"
    assert fixture["public_demo_corpus_version"] == "public-demo-corpus-v1"
    assert len(fixture["public_demo_source_register"]) >= 15
    assert len(fixture["documents"]) == 10

    for source in fixture["public_demo_source_register"]:
        assert source["source_url_or_locator"].startswith("https://")
        assert source["captured_at"] == "2026-05-23"
        assert source["extracted_fact"]
        assert source["demo_use"]
        assert source["limitation"]
