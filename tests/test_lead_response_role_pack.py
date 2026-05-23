import json
from pathlib import Path

from tests.fixtures.pilot_data import lead_response_role_pack_definition


def test_lead_response_role_pack_definition_is_complete() -> None:
    role_pack = lead_response_role_pack_definition()

    assert role_pack.role == "lead_response_operator"
    assert "Lead-response operator" in role_pack.title
    assert len(role_pack.missions) == 4
    assert len(role_pack.guardrail_questions) >= 3
    assert len(role_pack.rubric_criteria) >= 5
    assert len(role_pack.allowed_examples) >= 3
    assert len(role_pack.forbidden_examples) >= 4

    mission_text = " ".join(
        mission.objective + " " + mission.instructions for mission in role_pack.missions
    )
    for required in [
        "Acknowledge",
        "Qualify",
        "insufficient_evidence",
        "human-review handoff",
    ]:
        assert required in mission_text

    for mission in role_pack.missions:
        assert mission.citation_urls
        assert all(url.startswith("https://") for url in mission.citation_urls)


def test_lead_response_role_pack_blocks_regulated_and_autonomous_claims() -> None:
    role_pack = lead_response_role_pack_definition()
    text = " ".join(
        role_pack.rubric_criteria
        + role_pack.allowed_examples
        + role_pack.forbidden_examples
    )

    for blocked in [
        "legal",
        "medical",
        "financial",
        "regulated compliance advice",
        "guaranteed outcome",
        "approved without human reviewer action",
        "real customer, employee, lead, or prospect data",
    ]:
        assert blocked in text


def test_seed_fixture_exposes_lead_response_role_pack_metadata() -> None:
    fixture = json.loads(
        Path("tests/fixtures/seed_training_documents.json").read_text()
    )
    role_pack = fixture["lead_response_role_pack"]

    assert role_pack["role"] == "lead_response_operator"
    assert len(role_pack["mission_ids"]) == 4
    assert "lead-response-insufficient-evidence" in role_pack["mission_ids"]
    assert "lead-response-human-handoff" in role_pack["mission_ids"]
    assert len(role_pack["citation_urls"]) >= 6
    assert all(url.startswith("https://") for url in role_pack["citation_urls"])


def test_solo_showcase_plan_documents_role_pack_artifact() -> None:
    plan = Path("docs/solo_showcase_plan.md").read_text()

    for required in [
        "## Lead-Response Role Pack",
        "lead-response-acknowledge",
        "lead-response-qualify",
        "lead-response-insufficient-evidence",
        "lead-response-human-handoff",
        "Guardrail quiz topics",
        "Rubric criteria",
        "Allowed examples",
        "Forbidden examples",
    ]:
        assert required in plan
