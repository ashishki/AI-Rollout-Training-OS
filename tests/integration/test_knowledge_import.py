from datetime import date

import pytest
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import SourceDocument
from ai_rollout_os.integrations.knowledge_import import (
    ImportedKnowledgeDocument,
    KnowledgeImportService,
)
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_imported_docs_require_approval(migrated_engine: Engine) -> None:
    provider = StaticKnowledgeProvider(
        provider_name="manual_upload_v2",
        documents=[
            ImportedKnowledgeDocument(
                external_id="policy-v2",
                title="AI Use Policy V2",
                document_type="company_policy",
                body_text="Imported policy text.",
                effective_date=date(2026, 5, 21),
            )
        ],
    )

    with Session(migrated_engine) as session:
        result = KnowledgeImportService(session).import_from_provider(
            provider=provider,
            actor=_operator_actor(),
        )
        session.commit()

    assert result.imported_count == 1
    assert result.approval_status == "pending"
    with Session(migrated_engine) as session:
        document = session.scalar(
            select(SourceDocument).where(
                SourceDocument.snapshot_id == result.snapshot_ids[0]
            )
        )
    assert document is not None
    assert document.logical_document_id == "manual_upload_v2_policy_v2"
    assert document.approval_status == "pending"
    assert document.approved_by is None
    assert document.approved_at is None


def test_import_failure_does_not_activate_partial_snapshot(
    migrated_engine: Engine,
) -> None:
    provider = FailingKnowledgeProvider()

    with Session(migrated_engine) as session:
        with pytest.raises(RuntimeError, match="provider unavailable"):
            KnowledgeImportService(session).import_from_provider(
                provider=provider,
                actor=_operator_actor(),
            )
        documents = session.scalars(select(SourceDocument)).all()
        session.commit()

    assert documents == []


def test_invalid_import_does_not_create_partial_documents(
    migrated_engine: Engine,
) -> None:
    provider = StaticKnowledgeProvider(
        provider_name="confluence",
        documents=[
            ImportedKnowledgeDocument(
                external_id="valid-sop",
                title="Support SOP",
                document_type="sop",
                body_text="Valid SOP text.",
                effective_date=date(2026, 5, 21),
            ),
            ImportedKnowledgeDocument(
                external_id="bad-doc",
                title="Unsupported",
                document_type="unsupported",
                body_text="Should not persist.",
                effective_date=date(2026, 5, 21),
            ),
        ],
    )

    with Session(migrated_engine) as session:
        with pytest.raises(HTTPException):
            KnowledgeImportService(session).import_from_provider(
                provider=provider,
                actor=_operator_actor(),
            )
        documents = session.scalars(select(SourceDocument)).all()
        session.commit()

    assert documents == []


class StaticKnowledgeProvider:
    def __init__(
        self, *, provider_name: str, documents: list[ImportedKnowledgeDocument]
    ) -> None:
        self.provider_name = provider_name
        self._documents = documents

    def fetch_documents(self) -> list[ImportedKnowledgeDocument]:
        return self._documents


class FailingKnowledgeProvider:
    provider_name = "google_drive"

    def fetch_documents(self) -> list[ImportedKnowledgeDocument]:
        raise RuntimeError("provider unavailable")


def _operator_actor() -> ActorContext:
    return ActorContext(
        actor_id="operator-1",
        role="operator",
        workspace_id="ws-1",
        trace_id="trace-knowledge-import",
    )
