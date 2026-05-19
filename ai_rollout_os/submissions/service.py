from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import MissionAssignment, Submission
from ai_rollout_os.submissions.models import RedactionApprovalCreate, SubmissionCreate
from ai_rollout_os.submissions.redaction import inspect_sensitive_text


class SubmissionService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_submission(
        self, mission_id: str, payload: SubmissionCreate, actor: ActorContext
    ) -> Submission:
        assignment = self._assignment_for_learner(
            mission_id, payload.assignment_id, actor
        )
        redaction = inspect_sensitive_text(payload.artifact_text)
        latest_version = self._session.scalar(
            select(func.max(Submission.version)).where(
                Submission.assignment_id == assignment.id,
                Submission.workspace_id == actor.workspace_id,
            )
        )
        submission = Submission(
            id=f"submission_{uuid4().hex}",
            workspace_id=actor.workspace_id,
            mission_template_id=mission_id,
            assignment_id=assignment.id,
            learner_id=actor.actor_id,
            artifact_text=payload.artifact_text,
            policy_snapshot_id=payload.policy_snapshot_id,
            rubric_id=payload.rubric_id,
            version=(latest_version or 0) + 1,
            review_state="blocked_for_review" if redaction.flagged else "submitted",
            redaction_status="flagged" if redaction.flagged else "clear",
        )
        self._session.add(submission)
        self._session.flush()
        AuditEventRepository(self._session).append(
            actor_id=actor.actor_id,
            action="submission.created",
            resource_type="submission",
            resource_id=submission.id,
            result="success",
            trace_id=actor.trace_id,
        )
        return submission

    def approve_for_feedback(
        self,
        submission_id: str,
        payload: RedactionApprovalCreate,
        actor: ActorContext,
    ) -> Submission:
        submission = self._session.scalar(
            select(Submission).where(
                Submission.id == submission_id,
                Submission.workspace_id == actor.workspace_id,
                Submission.redaction_status == "flagged",
            )
        )
        if submission is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Submission not found"
            )
        submission.redaction_status = "approved"
        submission.review_state = "approved_for_feedback"
        AuditEventRepository(self._session).append(
            actor_id=actor.actor_id,
            action="submission.redaction_approved",
            resource_type="submission",
            resource_id=submission.id,
            result="success",
            trace_id=actor.trace_id,
            details=payload.note,
        )
        self._session.flush()
        return submission

    def _assignment_for_learner(
        self, mission_id: str, assignment_id: str, actor: ActorContext
    ) -> MissionAssignment:
        assignment = self._session.scalar(
            select(MissionAssignment).where(
                MissionAssignment.id == assignment_id,
                MissionAssignment.mission_template_id == mission_id,
                MissionAssignment.workspace_id == actor.workspace_id,
                MissionAssignment.learner_id == actor.actor_id,
            )
        )
        if assignment is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return assignment
