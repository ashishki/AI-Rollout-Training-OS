from ai_rollout_os.db.models import AuditEvent, Submission
from ai_rollout_os.feedback.engine import RubricEvaluationEngine
from ai_rollout_os.retrieval.evidence import RetrievalResult
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_insufficient_evidence_routes_to_human_review(
    migrated_engine: Engine,
) -> None:
    with Session(migrated_engine) as session:
        submission = Submission(
            id="submission-1",
            workspace_id="ws-1",
            mission_template_id="mission-1",
            assignment_id="assignment-1",
            learner_id="learner-1",
            artifact_text="Draft workflow artifact.",
            policy_snapshot_id="snapshot-1",
            rubric_id="rubric-1",
            version=1,
            review_state="submitted",
            redaction_status="clear",
        )
        session.add(submission)
        session.commit()

        record = RubricEvaluationEngine(session).evaluate_submission(
            submission_id=submission.id,
            retrieval_result=RetrievalResult(
                status="insufficient_evidence",
                evidence=[],
                generated_answer=None,
                reason="no_chunk_above_threshold",
            ),
        )
        session.commit()

        stored = session.scalar(
            select(Submission).where(Submission.id == submission.id)
        )
        audit_event = session.scalar(
            select(AuditEvent).where(AuditEvent.action == "feedback.needs_human_review")
        )

    assert record.feedback_status == "needs_human_review"
    assert record.learner_feedback is None
    assert record.validation_status == "insufficient_evidence"
    assert stored is not None
    assert stored.review_state == "needs_human_review"
    assert audit_event is not None
    assert audit_event.resource_id == "submission-1"
