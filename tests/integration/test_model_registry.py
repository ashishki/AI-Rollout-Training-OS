from ai_rollout_os.core.config import Settings
from ai_rollout_os.db.models import (
    FeedbackResult,
    ModelRegistryRecord,
    RetrievalCorpusVersion,
)
from ai_rollout_os.feedback.jobs import FeedbackJobService
from ai_rollout_os.feedback.model_registry import (
    FEEDBACK_PROMPT_VERSION,
    FEEDBACK_SCHEMA_VERSION,
)
from ai_rollout_os.jobs.models import FeedbackJobStatus, GeneratedFeedback
from ai_rollout_os.jobs.worker import FeedbackWorker
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session
from tests.integration.test_feedback_jobs import ready_submission


def test_feedback_result_records_versions(migrated_engine: Engine) -> None:
    with Session(migrated_engine) as session:
        submission = ready_submission()
        submission.policy_snapshot_id = "snapshot-registry"
        submission.rubric_id = "rubric-registry"
        session.add(submission)
        session.add(
            RetrievalCorpusVersion(
                id="corpus-registry-v3",
                workspace_id="ws-1",
                source_id="source-registry",
                source_document_id="doc-registry",
                snapshot_id="snapshot-registry",
                version=3,
                index_schema_version="v1",
                embedding_model="test-embedding-model",
                embedding_dimensions=8,
                chunk_count=4,
            )
        )
        session.commit()
        FeedbackJobService(session).enqueue_ready_submission(
            submission_id=submission.id
        )
        session.commit()

        worker = FeedbackWorker(
            session=session,
            settings=Settings(model_fast="registry-fast-model"),
            evaluator=lambda _job: GeneratedFeedback(
                feedback_status="ready_for_manager_review",
                learner_feedback="Use approved evidence.",
                validation_status="valid",
                risk_flags=[],
            ),
        )
        job = worker.run_one()
        assert job is not None
        job_status = job.status
        session.commit()

        result = session.scalar(select(FeedbackResult))
        records = session.scalars(select(ModelRegistryRecord)).all()

    assert job_status == FeedbackJobStatus.COMPLETED
    assert result is not None
    assert result.prompt_version == FEEDBACK_PROMPT_VERSION
    assert result.model_version == "registry-fast-model"
    assert result.rubric_version == "rubric:rubric-registry"
    assert result.corpus_version == "v1:3:snapshot-registry"
    assert result.feedback_schema_version == FEEDBACK_SCHEMA_VERSION
    assert {(record.registry_type, record.version) for record in records} == {
        ("prompt", FEEDBACK_PROMPT_VERSION),
        ("model", "registry-fast-model"),
        ("rubric", "rubric:rubric-registry"),
        ("retrieval_corpus", "v1:3:snapshot-registry"),
        ("feedback_schema", FEEDBACK_SCHEMA_VERSION),
    }
