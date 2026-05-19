from fastapi import FastAPI
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from ai_rollout_os.core.config import Settings, get_settings
from ai_rollout_os.reporting.report_routes import router as report_router
from ai_rollout_os.reporting.routes import router as reporting_router
from ai_rollout_os.retrieval.document_routes import router as document_router
from ai_rollout_os.submissions.review_routes import router as review_router
from ai_rollout_os.submissions.routes import router as submissions_router
from ai_rollout_os.training.cohort_routes import router as cohort_router
from ai_rollout_os.training.guardrail_routes import router as guardrail_router
from ai_rollout_os.training.routes import router as training_router


def create_app(
    settings: Settings | None = None,
    session_factory: sessionmaker[Session] | None = None,
) -> FastAPI:
    app_settings = settings or get_settings()
    if session_factory is None:
        engine = create_engine(app_settings.database_url)
        session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = FastAPI(title="AI Rollout Training OS")
    app.state.settings = app_settings
    app.state.session_factory = session_factory

    # Public by architecture and contract: liveness must not require auth.
    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok", "service": app_settings.service_name}

    app.include_router(cohort_router)
    app.include_router(document_router)
    app.include_router(guardrail_router)
    app.include_router(report_router)
    app.include_router(reporting_router)
    app.include_router(review_router)
    app.include_router(submissions_router)
    app.include_router(training_router)
    return app


app = create_app()
