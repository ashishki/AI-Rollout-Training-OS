from ai_rollout_os.db.models import FeedbackResult, ProgressReport, Submission
from ai_rollout_os.governance.risk_taxonomy import RISK_TAXONOMY_VERSION
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_dashboard import (
    auth_headers,
    dashboard_client,
    seed_dashboard_data,
)


def test_risk_flags_use_taxonomy(migrated_engine: Engine) -> None:
    client = dashboard_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        submission = session.scalar(
            select(Submission).where(Submission.id == "submission-1")
        )
        assert submission is not None
        submission.approved_workflow_change = "Reusable safe workflow."
        session.add(
            FeedbackResult(
                id="feedback-taxonomy",
                workspace_id="ws-1",
                submission_id="submission-1",
                submission_version=1,
                feedback_status="ready_for_manager_review",
                learner_feedback="Use approved evidence.",
                validation_status="valid",
                risk_flags=["pii", "missing_evidence", "customer_data"],
            )
        )
        session.commit()

    response = client.post(
        "/manager/cohorts/cohort-1/reports",
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["json_body"]["risk_taxonomy_version"] == RISK_TAXONOMY_VERSION
    assert payload["json_body"]["open_risk_flags"] == [
        "customer_data",
        "privacy",
        "unsupported_claim",
    ]
    assert "- unsupported_claim" in payload["markdown_body"]


def test_unknown_risk_flag_rejected(migrated_engine: Engine) -> None:
    client = dashboard_client(migrated_engine)
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        session.add(
            FeedbackResult(
                id="feedback-unknown-risk",
                workspace_id="ws-1",
                submission_id="submission-1",
                submission_version=1,
                feedback_status="ready_for_manager_review",
                learner_feedback="Use approved evidence.",
                validation_status="valid",
                risk_flags=["made_up_risk"],
            )
        )
        session.commit()

    response = client.post(
        "/manager/cohorts/cohort-1/reports",
        headers=auth_headers("manager-1", "manager"),
    )

    assert response.status_code == 422
    with Session(migrated_engine) as session:
        reports = session.scalars(select(ProgressReport)).all()
    assert reports == []
