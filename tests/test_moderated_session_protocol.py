from __future__ import annotations

import json
from pathlib import Path

PROTOCOL_PATH = Path("docs/MODERATED_SESSION_PROTOCOL.md")
LOG_PATH = Path("docs/evidence/moderated_session_log.json")


def test_moderated_session_log_does_not_invent_participants() -> None:
    log = json.loads(LOG_PATH.read_text(encoding="utf-8"))

    assert log["schema_version"] == "ship-it-moderated-session-log-v1"
    assert log["external_gate"] == "consented_real_participant_required"
    assert log["moderated_session_count"] == len(log["records"]) == 0
    assert set(log["blocked_claims"].values()) == {False}


def test_protocol_defines_privacy_rubric_and_nonclaims() -> None:
    protocol = PROTOCOL_PATH.read_text(encoding="utf-8")
    normalized_protocol = " ".join(protocol.split())

    for required in (
        "consenting adult participant",
        "random session code",
        "Boundary recognition",
        "Action choice",
        "Consequence reasoning",
        "Safer alternative",
        "self-authored dry run",
        "canonical session count is zero",
    ):
        assert required in normalized_protocol

    readme = Path("README.md").read_text(encoding="utf-8")
    assert "`0`\nrecorded moderated sessions" in readme
    assert "feature-frozen" in readme
