from collections.abc import Generator

from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session

from ai_rollout_os.auth.permissions import require_permission
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.reporting.reports import ReportRead, ReportService, report_read

router = APIRouter(prefix="/manager")
CREATE_REPORT = Depends(require_permission("manager.reports.create"))


def get_session(request: Request) -> Generator[Session]:
    session_factory = request.app.state.session_factory
    with session_factory() as session:
        yield session


DB_SESSION = Depends(get_session)


@router.post("/cohorts/{cohort_id}/reports", response_model=ReportRead, status_code=201)
def create_report(
    cohort_id: str,
    actor: ActorContext = CREATE_REPORT,
    session: Session = DB_SESSION,
) -> ReportRead:
    report = ReportService(session).create_report(cohort_id=cohort_id, actor=actor)
    session.commit()
    return report_read(report)
