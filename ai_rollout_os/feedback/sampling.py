from uuid import uuid4

from fastapi import HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import (
    FeedbackAdjudicationLabel,
    FeedbackResult,
    FeedbackSampleReview,
)

AUTHORIZED_REVIEWER_ROLES = {"manager", "operator"}
QUEUED = "queued"
ADJUDICATED = "adjudicated"


class FeedbackSampleRead(BaseModel):
    id: str
    feedback_result_id: str
    submission_id: str
    status: str
    prompt_version: str
    model_version: str
    rubric_version: str
    corpus_version: str
    feedback_schema_version: str
    risk_flags: list[str]


class AdjudicationCreate(BaseModel):
    faithfulness_label: str
    completeness_label: str
    relevance_label: str
    unsupported_claim: bool


class AdjudicationRead(BaseModel):
    id: str
    sample_review_id: str
    feedback_result_id: str
    adjudicator_id: str
    eval_dataset_record: dict


class FeedbackSamplingService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_review_items(
        self, *, actor: ActorContext, limit: int = 10
    ) -> list[FeedbackSampleRead]:
        _require_reviewer(actor)
        existing_feedback_ids = set(
            self._session.scalars(
                select(FeedbackSampleReview.feedback_result_id).where(
                    FeedbackSampleReview.workspace_id == actor.workspace_id
                )
            ).all()
        )
        query = (
            select(FeedbackResult)
            .where(FeedbackResult.workspace_id == actor.workspace_id)
            .order_by(FeedbackResult.created_at, FeedbackResult.id)
        )
        results = [
            result
            for result in self._session.scalars(query).all()
            if result.id not in existing_feedback_ids
        ][:limit]
        reviews = [
            FeedbackSampleReview(
                id=f"feedback_sample_{uuid4().hex}",
                workspace_id=actor.workspace_id,
                feedback_result_id=result.id,
                submission_id=result.submission_id,
                status=QUEUED,
                sampled_by=actor.actor_id,
            )
            for result in results
        ]
        self._session.add_all(reviews)
        self._session.flush()
        return [
            _sample_read(review, result)
            for review, result in zip(reviews, results, strict=True)
        ]

    def adjudicate(
        self,
        *,
        sample_review_id: str,
        payload: AdjudicationCreate,
        actor: ActorContext,
    ) -> AdjudicationRead:
        _require_reviewer(actor)
        review = self._session.scalar(
            select(FeedbackSampleReview).where(
                FeedbackSampleReview.id == sample_review_id,
                FeedbackSampleReview.workspace_id == actor.workspace_id,
            )
        )
        if review is None:
            raise ValueError("Feedback sample review not found")
        result = self._session.scalar(
            select(FeedbackResult).where(
                FeedbackResult.id == review.feedback_result_id,
                FeedbackResult.workspace_id == actor.workspace_id,
            )
        )
        if result is None:
            raise ValueError("Feedback result not found")
        record = _eval_dataset_record(result, payload)
        label = FeedbackAdjudicationLabel(
            id=f"feedback_adjudication_{uuid4().hex}",
            workspace_id=actor.workspace_id,
            sample_review_id=review.id,
            feedback_result_id=result.id,
            adjudicator_id=actor.actor_id,
            faithfulness_label=payload.faithfulness_label,
            completeness_label=payload.completeness_label,
            relevance_label=payload.relevance_label,
            unsupported_claim=payload.unsupported_claim,
            eval_dataset_record=record,
        )
        review.status = ADJUDICATED
        self._session.add(label)
        self._session.flush()
        return AdjudicationRead(
            id=label.id,
            sample_review_id=label.sample_review_id,
            feedback_result_id=label.feedback_result_id,
            adjudicator_id=label.adjudicator_id,
            eval_dataset_record=label.eval_dataset_record,
        )


def _require_reviewer(actor: ActorContext) -> None:
    if actor.role not in AUTHORIZED_REVIEWER_ROLES:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
        )


def _sample_read(
    review: FeedbackSampleReview, result: FeedbackResult
) -> FeedbackSampleRead:
    return FeedbackSampleRead(
        id=review.id,
        feedback_result_id=result.id,
        submission_id=result.submission_id,
        status=review.status,
        prompt_version=result.prompt_version,
        model_version=result.model_version,
        rubric_version=result.rubric_version,
        corpus_version=result.corpus_version,
        feedback_schema_version=result.feedback_schema_version,
        risk_flags=result.risk_flags,
    )


def _eval_dataset_record(result: FeedbackResult, payload: AdjudicationCreate) -> dict:
    return {
        "feedback_result_id": result.id,
        "submission_id": result.submission_id,
        "submission_version": result.submission_version,
        "prompt_version": result.prompt_version,
        "model_version": result.model_version,
        "rubric_version": result.rubric_version,
        "corpus_version": result.corpus_version,
        "feedback_schema_version": result.feedback_schema_version,
        "labels": {
            "faithfulness": payload.faithfulness_label,
            "completeness": payload.completeness_label,
            "relevance": payload.relevance_label,
            "unsupported_claim": payload.unsupported_claim,
        },
    }
