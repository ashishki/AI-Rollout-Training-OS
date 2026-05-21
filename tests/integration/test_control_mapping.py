from datetime import UTC, date, datetime

from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import FeedbackResult, SourceDocument, Submission
from ai_rollout_os.governance.controls import (
    CONTROL_MAPPING_VERSION,
    ControlMappingService,
)
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_dashboard import (
    auth_headers,
    dashboard_client,
    seed_dashboard_data,
)


def test_control_mapping_export_has_lineage(migrated_engine: Engine) -> None:
    export = _create_control_mapping_export(migrated_engine)

    assert export.version == CONTROL_MAPPING_VERSION
    assert export.report_id
    assert {document.id for document in export.source_documents} == {"document-1"}
    assert {submission.id for submission in export.submissions} == {
        "submission-1",
        "submission-2",
    }
    assert {result.id for result in export.feedback_results} == {"feedback-lineage-1"}
    assert {approval.ref for approval in export.approvals} == {
        "source_document:document-1",
        "submission:submission-1",
        "submission:submission-2",
    }
    for control in export.controls:
        assert control.evidence.source_document_ids == ["document-1"]
        assert set(control.evidence.submission_ids) == {
            "submission-1",
            "submission-2",
        }
        assert control.evidence.feedback_result_ids == ["feedback-lineage-1"]
        assert control.evidence.approval_refs
        assert control.evidence.report_ids == [export.report_id]


def test_lineage_export_excludes_raw_artifacts(migrated_engine: Engine) -> None:
    export = _create_control_mapping_export(migrated_engine)

    serialized = export.model_dump_json()
    assert "Draft workflow artifact." not in serialized
    assert "Sensitive draft workflow artifact." not in serialized
    assert "Private policy body text." not in serialized
    assert "Reusable customer-safe reply workflow." not in serialized
    assert "Manager note with proprietary context." not in serialized


def _create_control_mapping_export(migrated_engine: Engine):
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
                id="feedback-lineage-1",
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
    report_id = response.json()["id"]

    with Session(migrated_engine) as session:
        return ControlMappingService(session).export_for_report(
            report_id=report_id,
            actor=ActorContext(
                actor_id="manager-1",
                role="manager",
                workspace_id="ws-1",
                trace_id="trace-control-mapping",
            ),
        )
