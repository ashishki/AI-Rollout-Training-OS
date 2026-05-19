from collections.abc import Generator

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ai_rollout_os.auth.permissions import require_role
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.reporting.dashboard import DashboardMetrics, DashboardService

router = APIRouter(prefix="/manager")
MANAGER_ACTOR = Depends(require_role("manager"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.get("/cohorts/{cohort_id}/dashboard", response_model=DashboardMetrics)
def cohort_dashboard(
    cohort_id: str,
    actor: ActorContext = MANAGER_ACTOR,
    session: Session = DB_SESSION,
) -> DashboardMetrics:
    return DashboardService(session).cohort_dashboard(
        cohort_id=cohort_id,
        workspace_id=actor.workspace_id,
    )
