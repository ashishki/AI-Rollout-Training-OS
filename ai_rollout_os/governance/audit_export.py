import hashlib
import json
from collections.abc import Iterable
from datetime import datetime
from typing import Any

from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import ProgressReport
from ai_rollout_os.governance.controls import (
    CONTROL_MAPPING_VERSION,
    ControlMappingExport,
    ControlMappingService,
)

AUDIT_EXPORT_VERSION = "audit-export-v1"
HASH_ALGORITHM = "sha256"


class AuditExportPackage(BaseModel):
    version: str
    metadata: dict[str, Any]
    controls: list[dict[str, Any]]
    lineage: dict[str, list[dict[str, Any]]]
    approvals: list[dict[str, Any]]
    reports: list[dict[str, Any]]
    hashes: dict[str, str]


class AuditExportService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def export_for_cohort(
        self, *, cohort_id: str, actor: ActorContext
    ) -> AuditExportPackage:
        reports = self._reports_for_cohort(cohort_id, actor.workspace_id)
        if not reports:
            raise ValueError("No reports found for cohort")
        control_exports = [
            ControlMappingService(self._session).export_for_report(
                report_id=report.id,
                actor=actor,
            )
            for report in reports
        ]
        return _package(
            scope={"cohort_id": cohort_id},
            workspace_id=actor.workspace_id,
            control_exports=control_exports,
        )

    def export_for_date_range(
        self,
        *,
        start_at: datetime,
        end_at: datetime,
        actor: ActorContext,
    ) -> AuditExportPackage:
        reports = self._session.scalars(
            select(ProgressReport)
            .where(
                ProgressReport.workspace_id == actor.workspace_id,
                ProgressReport.created_at >= start_at,
                ProgressReport.created_at < end_at,
            )
            .order_by(
                ProgressReport.cohort_id,
                ProgressReport.version,
                ProgressReport.id,
            )
        ).all()
        if not reports:
            raise ValueError("No reports found for date range")
        control_exports = [
            ControlMappingService(self._session).export_for_report(
                report_id=report.id,
                actor=actor,
            )
            for report in reports
        ]
        return _package(
            scope={
                "start_at": start_at.isoformat(),
                "end_at": end_at.isoformat(),
            },
            workspace_id=actor.workspace_id,
            control_exports=control_exports,
        )

    def _reports_for_cohort(
        self, cohort_id: str, workspace_id: str
    ) -> list[ProgressReport]:
        return self._session.scalars(
            select(ProgressReport)
            .where(
                ProgressReport.cohort_id == cohort_id,
                ProgressReport.workspace_id == workspace_id,
            )
            .order_by(ProgressReport.version, ProgressReport.id)
        ).all()


def _package(
    *,
    scope: dict[str, Any],
    workspace_id: str,
    control_exports: list[ControlMappingExport],
) -> AuditExportPackage:
    report_ids = [export.report_id for export in control_exports]
    metadata = {
        "workspace_id": workspace_id,
        "scope": scope,
        "report_ids": report_ids,
        "control_mapping_version": CONTROL_MAPPING_VERSION,
        "hash_algorithm": HASH_ALGORITHM,
    }
    controls = [
        {
            "report_id": export.report_id,
            **control.model_dump(mode="json"),
        }
        for export in control_exports
        for control in export.controls
    ]
    lineage = {
        "source_documents": _dedupe(
            document
            for export in control_exports
            for document in export.source_documents
        ),
        "submissions": _dedupe(
            submission
            for export in control_exports
            for submission in export.submissions
        ),
        "feedback_results": _dedupe(
            result for export in control_exports for result in export.feedback_results
        ),
    }
    approvals = _dedupe(
        approval for export in control_exports for approval in export.approvals
    )
    reports = _dedupe(report for export in control_exports for report in export.reports)
    body = {
        "version": AUDIT_EXPORT_VERSION,
        "metadata": metadata,
        "controls": controls,
        "lineage": lineage,
        "approvals": approvals,
        "reports": reports,
    }
    hashes = {
        "metadata": _sha256(metadata),
        "controls": _sha256(controls),
        "lineage": _sha256(lineage),
        "approvals": _sha256(approvals),
        "reports": _sha256(reports),
    }
    hashes["package"] = _sha256({**body, "hashes": hashes})
    return AuditExportPackage(**body, hashes=hashes)


def _dedupe(items: Iterable[BaseModel]) -> list[dict[str, Any]]:
    deduped: dict[str, dict[str, Any]] = {}
    for item in items:
        payload = item.model_dump(mode="json")
        key = payload.get("id") or payload.get("ref")
        if key is None:
            key = _canonical_json(payload)
        deduped[str(key)] = payload
    return [deduped[key] for key in sorted(deduped)]


def _sha256(payload: Any) -> str:
    return hashlib.sha256(_canonical_json(payload).encode()).hexdigest()


def _canonical_json(payload: Any) -> str:
    return json.dumps(payload, sort_keys=True, separators=(",", ":"))
