from datetime import UTC, datetime

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import (
    FeedbackResult,
    MissionTemplate,
    QuizResult,
    Submission,
)
from ai_rollout_os.submissions.models import (
    ManagerApprovalCreate,
    ManagerSubmissionRead,
)


class ManagerReviewService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def list_submissions(
        self,
        *,
        actor: ActorContext,
        learner_id: str | None = None,
        mission_id: str | None = None,
        feedback_status: str | None = None,
        guardrail_status: str | None = None,
        risk_flag: str | None = None,
    ) -> list[ManagerSubmissionRead]:
        query = (
            select(Submission, FeedbackResult)
            .outerjoin(
                FeedbackResult,
                and_(
                    FeedbackResult.submission_id == Submission.id,
                    FeedbackResult.submission_version == Submission.version,
                ),
            )
            .where(Submission.workspace_id == actor.workspace_id)
        )
        if learner_id is not None:
            query = query.where(Submission.learner_id == learner_id)
        if mission_id is not None:
            query = query.where(Submission.mission_template_id == mission_id)

        rows = self._session.execute(query).all()
        items = [self._read_model(submission, result) for submission, result in rows]
        if feedback_status is not None:
            items = [item for item in items if item.feedback_status == feedback_status]
        if guardrail_status is not None:
            items = [
                item for item in items if item.guardrail_status == guardrail_status
            ]
        if risk_flag is not None:
            items = [item for item in items if risk_flag in item.risk_flags]
        return items

    def approve_submission(
        self,
        *,
        submission_id: str,
        payload: ManagerApprovalCreate,
        actor: ActorContext,
    ) -> ManagerSubmissionRead:
        submission = self._require_submission(submission_id, actor)
        submission.approval_status = "approved"
        submission.approval_note = payload.approval_note
        submission.manager_id = actor.actor_id
        submission.approved_at = datetime.now(UTC)
        submission.approved_workflow_change = payload.approved_workflow_change
        AuditEventRepository(self._session).append(
            actor_id=actor.actor_id,
            action="submission.workflow_change_approved",
            resource_type="submission",
            resource_id=submission.id,
            result="success",
            trace_id=actor.trace_id,
        )
        self._session.flush()
        result = self._feedback_result_for(submission)
        return self._read_model(submission, result)

    def _require_submission(
        self, submission_id: str, actor: ActorContext
    ) -> Submission:
        submission = self._session.scalar(
            select(Submission).where(
                Submission.id == submission_id,
                Submission.workspace_id == actor.workspace_id,
            )
        )
        if submission is None:
            raise ValueError("Submission not found")
        return submission

    def _read_model(
        self, submission: Submission, result: FeedbackResult | None
    ) -> ManagerSubmissionRead:
        return ManagerSubmissionRead(
            id=submission.id,
            learner_id=submission.learner_id,
            mission_id=submission.mission_template_id,
            feedback_status=result.feedback_status if result else "pending",
            guardrail_status=self._guardrail_status(submission),
            risk_flags=result.risk_flags if result else [],
            approval_status=submission.approval_status,
            manager_id=submission.manager_id,
            approved_at=submission.approved_at.isoformat()
            if submission.approved_at
            else None,
            approval_note=submission.approval_note,
            approved_workflow_change=submission.approved_workflow_change,
        )

    def _feedback_result_for(self, submission: Submission) -> FeedbackResult | None:
        return self._session.scalar(
            select(FeedbackResult).where(
                FeedbackResult.submission_id == submission.id,
                FeedbackResult.submission_version == submission.version,
            )
        )

    def _guardrail_status(self, submission: Submission) -> str:
        mission = self._session.scalar(
            select(MissionTemplate).where(
                MissionTemplate.id == submission.mission_template_id
            )
        )
        if mission is None:
            return "not_taken"
        result = self._session.scalar(
            select(QuizResult)
            .where(
                QuizResult.quiz_id == mission.guardrail_quiz_id,
                QuizResult.learner_id == submission.learner_id,
                QuizResult.workspace_id == submission.workspace_id,
            )
            .order_by(QuizResult.created_at.desc())
            .limit(1)
        )
        if result is None:
            return "not_taken"
        return "passed" if result.passed else "failed"
