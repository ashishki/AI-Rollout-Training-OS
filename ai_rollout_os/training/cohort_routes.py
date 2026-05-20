from collections.abc import Generator

from ai_rollout_os.auth.permissions import audit_denied_access, require_permission
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.training.cohort_models import (
    AssignmentRead,
    CohortCreate,
    CohortRead,
)
from ai_rollout_os.training.cohort_service import CohortService
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

router = APIRouter()
CREATE_COHORT = Depends(require_permission("cohorts.create"))
LAUNCH_COHORT = Depends(require_permission("cohorts.launch"))
READ_ASSIGNMENTS = Depends(require_permission("cohorts.assignments.read"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.post("/cohorts", response_model=CohortRead, status_code=201)
def create_cohort(
    payload: CohortCreate,
    actor: ActorContext = CREATE_COHORT,
    session: Session = DB_SESSION,
) -> CohortRead:
    cohort = CohortService(session).create_cohort(payload, actor)
    session.commit()
    return cohort_read(cohort, payload.learner_ids)


@router.post("/cohorts/{cohort_id}/launch", response_model=list[AssignmentRead])
def launch_cohort(
    cohort_id: str,
    actor: ActorContext = LAUNCH_COHORT,
    session: Session = DB_SESSION,
) -> list[AssignmentRead]:
    assignments = CohortService(session).launch_cohort(cohort_id, actor)
    session.commit()
    return [assignment_read(assignment) for assignment in assignments]


@router.get("/cohorts/{cohort_id}/assignments", response_model=list[AssignmentRead])
def learner_assignments(
    cohort_id: str,
    request: Request,
    actor: ActorContext = READ_ASSIGNMENTS,
    session: Session = DB_SESSION,
) -> list[AssignmentRead]:
    try:
        assignments = CohortService(session).learner_assignments(cohort_id, actor)
    except HTTPException as exc:
        if exc.status_code == 403:
            audit_denied_access(
                request=request,
                actor=actor,
                resource_type="cohort",
                resource_id=cohort_id,
            )
        raise
    return [assignment_read(assignment) for assignment in assignments]


def cohort_read(cohort, learner_ids: list[str]) -> CohortRead:
    return CohortRead(
        id=cohort.id,
        workspace_id=cohort.workspace_id,
        role_pack_id=cohort.role_pack_id,
        role_pack_version=cohort.role_pack_version,
        manager_id=cohort.manager_id,
        start_date=cohort.start_date,
        due_date=cohort.due_date,
        status=cohort.status,
        learner_ids=learner_ids,
    )


def assignment_read(assignment) -> AssignmentRead:
    return AssignmentRead(
        id=assignment.id,
        cohort_id=assignment.cohort_id,
        learner_id=assignment.learner_id,
        mission_template_id=assignment.mission_template_id,
        role_pack_version=assignment.role_pack_version,
        status=assignment.status,
    )
