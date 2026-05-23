from pathlib import Path


def test_solo_rollout_readiness_review_cites_required_artifacts() -> None:
    review = Path("docs/audit/SOLO_ROLLOUT_READINESS_REVIEW.md").read_text()
    index = Path("docs/audit/AUDIT_INDEX.md").read_text()

    assert "# Solo Rollout Readiness Review" in review
    assert "Status: READY FOR INTERNAL HANDOFF" in review
    assert "## Evidence Links" in review
    assert "docs/public_corpus/ai_rollout_source_register.md" in review
    assert "docs/solo_showcase_plan.md#lead-response-role-pack" in review
    assert "docs/solo_showcase_artifacts/mini_cohort_replay.md" in review
    assert "docs/solo_showcase_artifacts/report.md" in review
    assert "docs/solo_showcase_plan.md#ux-demo-gap-decision" in review
    assert "SOLO-ROLLOUT-READINESS" in index
    assert "docs/audit/SOLO_ROLLOUT_READINESS_REVIEW.md" in index


def test_solo_rollout_readiness_review_records_next_action_and_limits() -> None:
    review = Path("docs/audit/SOLO_ROLLOUT_READINESS_REVIEW.md").read_text()

    assert "Next action: hand off to Lead Response SLA Agent" in review
    assert "READY FOR INTERNAL HANDOFF" in review
    assert "P2-UX-001 remains open" in review
    assert "does not prove real adoption" in review
    assert "Do not use it for GA claims" in review
    assert "productivity claims" in review
