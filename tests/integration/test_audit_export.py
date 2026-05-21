from datetime import UTC, date, datetime

from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import FeedbackResult, SourceDocument, Submission
from ai_rollout_os.governance.audit_export import (
    AUDIT_EXPORT_VERSION,
    HASH_ALGORITHM,
    AuditExportService,
)
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_dashboard import (
    auth_headers,
    dashboard_client,
    seed_dashboard_data,
)


def test_audit_export_package_complete(migrated_engine: Engine) -> None:
    report_id = _seed_audit_export_report(migrated_engine)

    with Session(migrated_engine) as session:
        package = AuditExportService(session).export_for_cohort(
            cohort_id="cohort-1",
            actor=_manager_actor(),
        )

    assert package.version == AUDIT_EXPORT_VERSION
    assert package.metadata == {
        "workspace_id": "ws-1",
        "scope": {"cohort_id": "cohort-1"},
        "report_ids": [report_id],
        "control_mapping_version": "control-mapping-v1",
        "hash_algorithm": HASH_ALGORITHM,
    }
    assert package.controls
    assert package.lineage["source_documents"][0]["id"] == "document-1"
    assert {submission["id"] for submission in package.lineage["submissions"]} == {
        "submission-1",
        "submission-2",
    }
    assert package.lineage["feedback_results"][0]["id"] == "feedback-export-1"
    assert {approval["ref"] for approval in package.approvals} == {
        "source_document:document-1",
        "submission:submission-1",
        "submission:submission-2",
    }
    assert package.reports[0]["id"] == report_id
    assert set(package.hashes) == {
        "metadata",
        "controls",
        "lineage",
        "approvals",
        "reports",
        "package",
    }
    assert all(len(value) == 64 for value in package.hashes.values())


def test_audit_export_is_reproducible(migrated_engine: Engine) -> None:
    _seed_audit_export_report(migrated_engine)

    with Session(migrated_engine) as session:
        first = AuditExportService(session).export_for_cohort(
            cohort_id="cohort-1",
            actor=_manager_actor(),
        )
        second = AuditExportService(session).export_for_cohort(
            cohort_id="cohort-1",
            actor=_manager_actor(),
        )

    assert first.hashes["package"] == second.hashes["package"]
    assert first.model_dump(mode="json") == second.model_dump(mode="json")


def _seed_audit_export_report(migrated_engine: Engine) -> str:
    client = dashboard_client(migrated_engine)
    now = datetime.now(UTC)
    with Session(migrated_engine) as session:
        seed_dashboard_data(session)
        session.add(
            SourceDocument(
                id="document-1",
                logical_document_id="policy-support",
                workspace_id="ws-1",
                title="Support Policy",
                document_type="policy",
                body_text="Private policy body text.",
                effective_date=date(2026, 5, 21),
                snapshot_id="snapshot-1",
                version=1,
                created_by="operator-1",
                approval_status="approved",
                approved_by="operator-1",
                approved_at=now,
            )
        )
        submission = session.scalar(
            select(Submission).where(Submission.id == "submission-1")
        )
        assert submission is not None
        submission.approved_workflow_change = "Reusable customer-safe reply workflow."
        submission.approval_note = "Manager note with proprietary context."
        submission.manager_id = "manager-1"
        submission.approved_at = now
        session.add(
            FeedbackResult(
                id="feedback-export-1",
                workspace_id="ws-1",
                submission_id="submission-1",
                submission_version=1,
                feedback_status="ready_for_manager_review",
                learner_feedback="Use approved evidence.",
                validation_status="valid",
                risk_flags=["privacy"],
            )
        )
        session.commit()

    response = client.post(
        "/manager/cohorts/cohort-1/reports",
        headers=auth_headers("manager-1", "manager"),
    )
    assert response.status_code == 201
    return str(response.json()["id"])


def _manager_actor() -> ActorContext:
    return ActorContext(
        actor_id="manager-1",
        role="manager",
        workspace_id="ws-1",
        trace_id="trace-audit-export",
    )
