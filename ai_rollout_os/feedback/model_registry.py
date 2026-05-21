from dataclasses import dataclass
from hashlib import sha256

from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.core.config import Settings
from ai_rollout_os.db.models import (
    FeedbackJob,
    ModelRegistryRecord,
    RetrievalCorpusVersion,
    Submission,
)

FEEDBACK_PROMPT_VERSION = "feedback-prompt-v1"
FEEDBACK_SCHEMA_VERSION = "feedback-schema-v1"


@dataclass(frozen=True)
class FeedbackVersionRefs:
    prompt_version: str
    model_version: str
    rubric_version: str
    corpus_version: str
    feedback_schema_version: str


class ModelRegistryService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def feedback_versions_for_job(
        self, *, job: FeedbackJob, settings: Settings
    ) -> FeedbackVersionRefs:
        submission = self._session.scalar(
            select(Submission).where(
                Submission.id == job.submission_id,
                Submission.version == job.submission_version,
                Submission.workspace_id == job.workspace_id,
            )
        )
        if submission is None:
            raise ValueError("Submission not found for feedback job")

        refs = FeedbackVersionRefs(
            prompt_version=FEEDBACK_PROMPT_VERSION,
            model_version=settings.model_fast,
            rubric_version=f"rubric:{submission.rubric_id}",
            corpus_version=self._corpus_version(submission),
            feedback_schema_version=FEEDBACK_SCHEMA_VERSION,
        )
        self._ensure_record(
            workspace_id=job.workspace_id,
            registry_type="prompt",
            version=refs.prompt_version,
            name="Feedback generation prompt",
            metadata={"owner": "feedback"},
        )
        self._ensure_record(
            workspace_id=job.workspace_id,
            registry_type="model",
            version=refs.model_version,
            name=settings.model_fast,
            metadata={"setting": "MODEL_FAST"},
        )
        self._ensure_record(
            workspace_id=job.workspace_id,
            registry_type="rubric",
            version=refs.rubric_version,
            name=submission.rubric_id,
            metadata={"rubric_id": submission.rubric_id},
        )
        self._ensure_record(
            workspace_id=job.workspace_id,
            registry_type="retrieval_corpus",
            version=refs.corpus_version,
            name=submission.policy_snapshot_id,
            metadata={"policy_snapshot_id": submission.policy_snapshot_id},
        )
        self._ensure_record(
            workspace_id=job.workspace_id,
            registry_type="feedback_schema",
            version=refs.feedback_schema_version,
            name="Structured feedback schema",
            metadata={"owner": "feedback"},
        )
        return refs

    def _corpus_version(self, submission: Submission) -> str:
        corpus = self._session.scalar(
            select(RetrievalCorpusVersion)
            .where(
                RetrievalCorpusVersion.workspace_id == submission.workspace_id,
                RetrievalCorpusVersion.snapshot_id == submission.policy_snapshot_id,
            )
            .order_by(
                RetrievalCorpusVersion.created_at.desc(),
                RetrievalCorpusVersion.id.desc(),
            )
            .limit(1)
        )
        if corpus is None:
            return f"snapshot:{submission.policy_snapshot_id}:unindexed"
        return f"{corpus.index_schema_version}:{corpus.version}:{corpus.snapshot_id}"

    def _ensure_record(
        self,
        *,
        workspace_id: str,
        registry_type: str,
        version: str,
        name: str,
        metadata: dict,
    ) -> None:
        existing = self._session.scalar(
            select(ModelRegistryRecord).where(
                ModelRegistryRecord.workspace_id == workspace_id,
                ModelRegistryRecord.registry_type == registry_type,
                ModelRegistryRecord.version == version,
            )
        )
        if existing is not None:
            return
        record = ModelRegistryRecord(
            id=_record_id(workspace_id, registry_type, version),
            workspace_id=workspace_id,
            registry_type=registry_type,
            version=version,
            name=name,
            registry_metadata=metadata,
        )
        self._session.add(record)


def _record_id(workspace_id: str, registry_type: str, version: str) -> str:
    digest = sha256(f"{workspace_id}|{registry_type}|{version}".encode()).hexdigest()
    return f"registry_{digest[:24]}"
