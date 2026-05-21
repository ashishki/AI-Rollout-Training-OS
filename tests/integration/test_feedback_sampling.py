import pytest
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import (
    FeedbackAdjudicationLabel,
    FeedbackResult,
    FeedbackSampleReview,
)
from ai_rollout_os.feedback.sampling import (
    AdjudicationCreate,
    FeedbackSamplingService,
)
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_manager_review import ready_submission


def test_sampling_respects_authorization(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        session.add(ready_submission())
        session.add(_feedback_result())
        session.commit()

        with pytest.raises(HTTPException) as exc_info:
            FeedbackSamplingService(session).create_review_items(
                actor=_actor("learner-1", "learner")
            )
        samples = FeedbackSamplingService(session).create_review_items(
            actor=_actor("manager-1", "manager")
        )
        session.commit()

    assert exc_info.value.status_code == 403
    assert len(samples) == 1
    serialized = samples[0].model_dump_json()
    assert "Draft workflow artifact." not in serialized
    assert "Use approved evidence." not in serialized
    assert "artifact_text" not in serialized
    assert samples[0].feedback_result_id == "feedback-result-sample"


def test_adjudication_preserves_original_feedback(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        session.add(ready_submission())
        session.add(_feedback_result())
        session.commit()

        sample = FeedbackSamplingService(session).create_review_items(
            actor=_actor("operator-1", "operator")
        )[0]
        adjudication = FeedbackSamplingService(session).adjudicate(
            sample_review_id=sample.id,
            payload=AdjudicationCreate(
                faithfulness_label="pass",
                completeness_label="partial",
                relevance_label="pass",
                unsupported_claim=False,
            ),
            actor=_actor("manager-1", "manager"),
        )
        session.commit()

        result = session.get(FeedbackResult, "feedback-result-sample")
        review = session.get(FeedbackSampleReview, sample.id)
        label = session.scalar(select(FeedbackAdjudicationLabel))

    assert result is not None
    assert result.learner_feedback == "Use approved evidence."
    assert result.validation_status == "valid"
    assert result.risk_flags == ["privacy"]
    assert review is not None
    assert review.status == "adjudicated"
    assert label is not None
    assert label.eval_dataset_record == adjudication.eval_dataset_record
    assert label.eval_dataset_record["feedback_result_id"] == "feedback-result-sample"
    assert "learner_feedback" not in label.eval_dataset_record


def _feedback_result() -> FeedbackResult:
    return FeedbackResult(
        id="feedback-result-sample",
        workspace_id="ws-1",
        submission_id="submission-1",
        submission_version=1,
        feedback_status="ready_for_manager_review",
        learner_feedback="Use approved evidence.",
        validation_status="valid",
        risk_flags=["privacy"],
        prompt_version="feedback-prompt-v1",
        model_version="test-model",
        rubric_version="rubric:rubric-1",
        corpus_version="v1:1:snapshot-1",
        feedback_schema_version="feedback-schema-v1",
    )


def _actor(actor_id: str, role: str) -> ActorContext:
    return ActorContext(
        actor_id=actor_id,
        role=role,
        workspace_id="ws-1",
        trace_id="trace-feedback-sampling",
    )
