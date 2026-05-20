from collections.abc import Generator

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ai_rollout_os.auth.permissions import require_permission
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.submissions.models import (
    RedactionApprovalCreate,
    SubmissionCreate,
    SubmissionRead,
)
from ai_rollout_os.submissions.service import SubmissionService

router = APIRouter()
CREATE_SUBMISSION = Depends(require_permission("submissions.create"))
APPROVE_REDACTION = Depends(require_permission("submissions.redaction_approval.create"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.post(
    "/missions/{mission_id}/submissions",
    response_model=SubmissionRead,
    status_code=201,
)
def create_submission(
    mission_id: str,
    payload: SubmissionCreate,
    actor: ActorContext = CREATE_SUBMISSION,
    session: Session = DB_SESSION,
) -> SubmissionRead:
    submission = SubmissionService(session).create_submission(
        mission_id, payload, actor
    )
    session.commit()
    return submission_read(submission)


@router.post(
    "/submissions/{submission_id}/redaction-approval",
    response_model=SubmissionRead,
)
def approve_redaction_for_feedback(
    submission_id: str,
    payload: RedactionApprovalCreate,
    actor: ActorContext = APPROVE_REDACTION,
    session: Session = DB_SESSION,
) -> SubmissionRead:
    submission = SubmissionService(session).approve_for_feedback(
        submission_id, payload, actor
    )
    session.commit()
    return submission_read(submission)


def submission_read(submission) -> SubmissionRead:
    return SubmissionRead(
        id=submission.id,
        workspace_id=submission.workspace_id,
        mission_template_id=submission.mission_template_id,
        assignment_id=submission.assignment_id,
        learner_id=submission.learner_id,
        artifact_text="[REDACTED]"
        if submission.redaction_status == "flagged"
        else submission.artifact_text,
        policy_snapshot_id=submission.policy_snapshot_id,
        rubric_id=submission.rubric_id,
        version=submission.version,
        review_state=submission.review_state,
        redaction_status=submission.redaction_status,
    )
