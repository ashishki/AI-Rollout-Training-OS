from dataclasses import dataclass
from datetime import date
from typing import Protocol
from uuid import uuid4

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import SourceDocument
from ai_rollout_os.retrieval.document_approval import PENDING_DOCUMENT_STATUS
from ai_rollout_os.retrieval.document_models import DOCUMENT_TYPES

SUPPORTED_KNOWLEDGE_PROVIDERS = {
    "google_drive",
    "confluence",
    "notion",
    "sharepoint",
    "manual_upload_v2",
}


@dataclass(frozen=True)
class ImportedKnowledgeDocument:
    external_id: str
    title: str
    document_type: str
    body_text: str
    effective_date: date


@dataclass(frozen=True)
class KnowledgeImportResult:
    provider: str
    imported_count: int
    snapshot_ids: list[str]
    approval_status: str


class KnowledgeImportProvider(Protocol):
    provider_name: str

    def fetch_documents(self) -> list[ImportedKnowledgeDocument]:
        pass


class KnowledgeImportService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def import_from_provider(
        self, *, provider: KnowledgeImportProvider, actor: ActorContext
    ) -> KnowledgeImportResult:
        provider_name = provider.provider_name.strip().lower()
        if provider_name not in SUPPORTED_KNOWLEDGE_PROVIDERS:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Unsupported knowledge provider",
            )

        imported_documents = provider.fetch_documents()
        self._validate_documents(imported_documents)

        documents = [
            _source_document(
                imported=document,
                provider_name=provider_name,
                actor=actor,
            )
            for document in imported_documents
        ]
        self._session.add_all(documents)
        self._session.flush()
        for document in documents:
            AuditEventRepository(self._session).append(
                actor_id=actor.actor_id,
                action="knowledge_document.imported",
                resource_type="source_document",
                resource_id=document.snapshot_id,
                result="success",
                trace_id=actor.trace_id,
                details=provider_name,
            )
        self._session.flush()
        return KnowledgeImportResult(
            provider=provider_name,
            imported_count=len(documents),
            snapshot_ids=[document.snapshot_id for document in documents],
            approval_status=PENDING_DOCUMENT_STATUS,
        )

    def _validate_documents(
        self, imported_documents: list[ImportedKnowledgeDocument]
    ) -> None:
        if not imported_documents:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="No documents returned by provider",
            )
        for document in imported_documents:
            if document.document_type not in DOCUMENT_TYPES:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Unsupported document type",
                )
            if not document.title.strip() or not document.body_text.strip():
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Invalid imported document",
                )


def _source_document(
    *,
    imported: ImportedKnowledgeDocument,
    provider_name: str,
    actor: ActorContext,
) -> SourceDocument:
    source_id = _safe_external_id(imported.external_id)
    return SourceDocument(
        id=f"docver_{uuid4().hex}",
        logical_document_id=f"{provider_name}_{source_id}",
        workspace_id=actor.workspace_id,
        title=imported.title,
        document_type=imported.document_type,
        body_text=imported.body_text,
        effective_date=imported.effective_date,
        snapshot_id=f"snapshot_{uuid4().hex}",
        version=1,
        created_by=actor.actor_id,
        approval_status=PENDING_DOCUMENT_STATUS,
    )


def _safe_external_id(external_id: str) -> str:
    normalized = "".join(
        char.lower() if char.isalnum() else "_" for char in external_id.strip()
    ).strip("_")
    return normalized[:48] or uuid4().hex
