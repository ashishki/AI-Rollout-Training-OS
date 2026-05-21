import os
from pathlib import Path

import pytest
from ai_rollout_os.core.config import TEST_DEFAULTS
from alembic import command
from alembic.config import Config
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine


def database_url() -> str:
    return os.environ.get("DATABASE_URL", TEST_DEFAULTS["DATABASE_URL"])


def alembic_config(url: str) -> Config:
    config = Config()
    config.set_main_option("script_location", str(Path("migrations")))
    config.set_main_option("sqlalchemy.url", url)
    return config


def reset_database(engine: Engine) -> None:
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS feedback_adjudication_labels"))
        connection.execute(text("DROP TABLE IF EXISTS feedback_sample_reviews"))
        connection.execute(text("DROP TABLE IF EXISTS reminder_jobs"))
        connection.execute(text("DROP TABLE IF EXISTS model_registry_records"))
        connection.execute(text("DROP TABLE IF EXISTS progress_reports"))
        connection.execute(text("DROP TABLE IF EXISTS feedback_results"))
        connection.execute(text("DROP TABLE IF EXISTS feedback_jobs"))
        connection.execute(text("DROP TABLE IF EXISTS retrieval_chunks"))
        connection.execute(text("DROP TABLE IF EXISTS retrieval_corpus_versions"))
        connection.execute(text("DROP TABLE IF EXISTS submissions"))
        connection.execute(text("DROP TABLE IF EXISTS quiz_results"))
        connection.execute(text("DROP TABLE IF EXISTS guardrail_questions"))
        connection.execute(text("DROP TABLE IF EXISTS mission_assignments"))
        connection.execute(text("DROP TABLE IF EXISTS cohort_enrollments"))
        connection.execute(text("DROP TABLE IF EXISTS cohorts"))
        connection.execute(text("DROP TABLE IF EXISTS source_documents"))
        connection.execute(text("DROP TABLE IF EXISTS mission_templates"))
        connection.execute(text("DROP TABLE IF EXISTS guardrail_quizzes"))
        connection.execute(text("DROP TABLE IF EXISTS rubrics"))
        connection.execute(text("DROP TABLE IF EXISTS role_packs"))
        connection.execute(text("DROP TABLE IF EXISTS audit_events"))
        connection.execute(text("DROP TABLE IF EXISTS users"))
        connection.execute(text("DROP TABLE IF EXISTS workspaces"))
        connection.execute(text("DROP TABLE IF EXISTS alembic_version"))


@pytest.fixture
def migrated_engine() -> Engine:
    url = database_url()
    engine = create_engine(url)
    reset_database(engine)
    command.upgrade(alembic_config(url), "head")
    try:
        yield engine
    finally:
        reset_database(engine)
        engine.dispose()
