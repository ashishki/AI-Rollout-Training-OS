from collections.abc import Generator

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ai_rollout_os.auth.permissions import require_permission
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.reporting.dashboard import DashboardMetrics, DashboardService

router = APIRouter(prefix="/manager")
READ_DASHBOARD = Depends(require_permission("manager.dashboard.read"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.get("/cohorts/{cohort_id}/dashboard", response_model=DashboardMetrics)
def cohort_dashboard(
    cohort_id: str,
    actor: ActorContext = READ_DASHBOARD,
    session: Session = DB_SESSION,
) -> DashboardMetrics:
    return DashboardService(session).cohort_dashboard(
        cohort_id=cohort_id,
        workspace_id=actor.workspace_id,
    )
