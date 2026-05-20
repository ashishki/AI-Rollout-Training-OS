from datetime import UTC, datetime, timedelta

from ai_rollout_os.db.models import (
    AuditEvent,
    FeedbackResult,
    SourceDocument,
    Submission,
    Workspace,
)
from ai_rollout_os.jobs.retention import REDACTED_BY_RETENTION, RetentionJob
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_retention_preserves_audit_events(migrated_engine: Engine) -> None:
    now = datetime(2026, 5, 20, tzinfo=UTC)
    old = now - timedelta(days=400)
    recent = now - timedelta(days=30)

    with Session(migrated_engine) as session:
        session.add(Workspace(id="ws-1", name="Pilot"))
        session.add(
            Submission(
                id="submission-old",
                workspace_id="ws-1",
                mission_template_id="mission-1",
                assignment_id="assignment-1",
                learner_id="learner-1",
                artifact_text="Sensitive old artifact",
                policy_snapshot_id="snapshot-1",
                rubric_id="rubric-1",
                version=1,
                review_state="submitted",
                redaction_status="clear",
                approval_note="Manager note",
                approved_workflow_change="Workflow detail",
                rejection_reason="Rejected detail",
                created_at=old,
            )
        )
        session.add(
            Submission(
                id="submission-recent",
                workspace_id="ws-1",
                mission_template_id="mission-1",
                assignment_id="assignment-2",
                learner_id="learner-1",
                artifact_text="Recent artifact",
                policy_snapshot_id="snapshot-1",
                rubric_id="rubric-1",
                version=1,
                review_state="submitted",
                redaction_status="clear",
                created_at=recent,
            )
        )
        session.add(
            FeedbackResult(
                id="feedback-old",
                workspace_id="ws-1",
                submission_id="submission-old",
                submission_version=1,
                feedback_status="complete",
                learner_feedback="Sensitive feedback",
                validation_status="valid",
                risk_flags=[],
                created_at=old,
            )
        )
        session.add(
            SourceDocument(
                id="source-old",
                logical_document_id="policy-1",
                workspace_id="ws-1",
                title="Policy",
                document_type="company_policy",
                body_text="Sensitive policy body",
                effective_date=now.date(),
                snapshot_id="snapshot-old",
                version=1,
                created_by="operator-1",
                created_at=old,
            )
        )
        session.add(
            AuditEvent(
                actor_id="learner-1",
                action="submission.created",
                resource_type="submission",
                resource_id="submission-old",
                result="success",
                trace_id="trace-original",
            )
        )
        session.commit()

        result = RetentionJob(session).redact_expired_artifacts(
            workspace_id="ws-1",
            retention_days=365,
            actor_id="system",
            trace_id="trace-retention",
            now=now,
        )
        session.commit()

    assert result.submissions_redacted == 1
    assert result.feedback_results_redacted == 1
    assert result.source_documents_redacted == 1
    with Session(migrated_engine) as session:
        old_submission = session.get(Submission, "submission-old")
        recent_submission = session.get(Submission, "submission-recent")
        old_feedback = session.get(FeedbackResult, "feedback-old")
        old_source = session.get(SourceDocument, "source-old")
        events = session.scalars(select(AuditEvent).order_by(AuditEvent.id)).all()

    assert old_submission is not None
    assert old_submission.artifact_text == REDACTED_BY_RETENTION
    assert old_submission.approval_note is None
    assert old_submission.approved_workflow_change is None
    assert old_submission.rejection_reason is None
    assert old_submission.redaction_status == "retention_redacted"
    assert recent_submission is not None
    assert recent_submission.artifact_text == "Recent artifact"
    assert old_feedback is not None
    assert old_feedback.learner_feedback == REDACTED_BY_RETENTION
    assert old_source is not None
    assert old_source.body_text == REDACTED_BY_RETENTION
    assert ("submission.created", "submission-old", "trace-original") in [
        (event.action, event.resource_id, event.trace_id) for event in events
    ]
    assert ("retention.redacted", "submission-old", "trace-retention") in [
        (event.action, event.resource_id, event.trace_id) for event in events
    ]
