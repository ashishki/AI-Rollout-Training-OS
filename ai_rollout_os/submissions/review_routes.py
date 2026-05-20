from collections.abc import Generator

from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.orm import Session

from ai_rollout_os.auth.permissions import require_permission
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.submissions.models import (
    ManagerApprovalCreate,
    ManagerSubmissionRead,
)
from ai_rollout_os.submissions.review_service import ManagerReviewService

router = APIRouter(prefix="/manager")
READ_MANAGER_SUBMISSIONS = Depends(require_permission("manager.submissions.read"))
APPROVE_MANAGER_SUBMISSION = Depends(require_permission("manager.submissions.approve"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.get("/submissions", response_model=list[ManagerSubmissionRead])
def list_manager_submissions(
    learner_id: str | None = Query(default=None),
    mission_id: str | None = Query(default=None),
    feedback_status: str | None = Query(default=None),
    guardrail_status: str | None = Query(default=None),
    risk_flag: str | None = Query(default=None),
    actor: ActorContext = READ_MANAGER_SUBMISSIONS,
    session: Session = DB_SESSION,
) -> list[ManagerSubmissionRead]:
    return ManagerReviewService(session).list_submissions(
        actor=actor,
        learner_id=learner_id,
        mission_id=mission_id,
        feedback_status=feedback_status,
        guardrail_status=guardrail_status,
        risk_flag=risk_flag,
    )


@router.post(
    "/submissions/{submission_id}/approve",
    response_model=ManagerSubmissionRead,
)
def approve_workflow_change(
    submission_id: str,
    payload: ManagerApprovalCreate,
    actor: ActorContext = APPROVE_MANAGER_SUBMISSION,
    session: Session = DB_SESSION,
) -> ManagerSubmissionRead:
    item = ManagerReviewService(session).approve_submission(
        submission_id=submission_id,
        payload=payload,
        actor=actor,
    )
    session.commit()
    return item
