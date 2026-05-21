from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.orm import Session

from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import (
    Cohort,
    FeedbackResult,
    MissionAssignment,
    ProgressReport,
    SourceDocument,
    Submission,
)
from ai_rollout_os.governance.risk_taxonomy import RISK_TAXONOMY_VERSION

CONTROL_MAPPING_VERSION = "control-mapping-v1"


class ControlEvidence(BaseModel):
    source_document_ids: list[str]
    submission_ids: list[str]
    feedback_result_ids: list[str]
    approval_refs: list[str]
    report_ids: list[str]


class ControlMapping(BaseModel):
    control_id: str
    title: str
    category: str
    evidence: ControlEvidence


class SourceDocumentLineage(BaseModel):
    id: str
    logical_document_id: str
    snapshot_id: str
    document_type: str
    version: int
    approval_status: str
    approved_by: str | None
    approved_at: str | None


class SubmissionLineage(BaseModel):
    id: str
    assignment_id: str
    learner_id: str
    policy_snapshot_id: str
    version: int
    review_state: str
    redaction_status: str
    approval_status: str


class FeedbackLineage(BaseModel):
    id: str
    submission_id: str
    submission_version: int
    feedback_status: str
    validation_status: str
    risk_flags: list[str]


class ApprovalLineage(BaseModel):
    ref: str
    approval_type: str
    subject_id: str
    status: str
    actor_id: str | None
    approved_at: str | None


class ReportLineage(BaseModel):
    id: str
    cohort_id: str
    version: int
    policy_snapshot_id: str
    created_by: str
    created_at: str | None
    risk_taxonomy_version: str | None


class ControlMappingExport(BaseModel):
    version: str
    workspace_id: str
    cohort_id: str
    report_id: str
    controls: list[ControlMapping]
    source_documents: list[SourceDocumentLineage]
    submissions: list[SubmissionLineage]
    feedback_results: list[FeedbackLineage]
    approvals: list[ApprovalLineage]
    reports: list[ReportLineage]


class ControlMappingService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def export_for_report(
        self, *, report_id: str, actor: ActorContext
    ) -> ControlMappingExport:
        report = self._require_report(report_id, actor.workspace_id)
        cohort = self._require_cohort(report.cohort_id, actor.workspace_id)
        submissions = self._cohort_submissions(cohort.id, actor.workspace_id)
        feedback_results = self._feedback_results(submissions, actor.workspace_id)
        source_documents = self._source_documents(submissions, actor.workspace_id)
        approvals = _approval_lineage(source_documents, submissions)
        return ControlMappingExport(
            version=CONTROL_MAPPING_VERSION,
            workspace_id=actor.workspace_id,
            cohort_id=cohort.id,
            report_id=report.id,
            controls=_controls(
                source_documents=source_documents,
                submissions=submissions,
                feedback_results=feedback_results,
                approvals=approvals,
                report=report,
            ),
            source_documents=[
                SourceDocumentLineage(
                    id=document.id,
                    logical_document_id=document.logical_document_id,
                    snapshot_id=document.snapshot_id,
                    document_type=document.document_type,
                    version=document.version,
                    approval_status=document.approval_status,
                    approved_by=document.approved_by,
                    approved_at=(
                        document.approved_at.isoformat()
                        if document.approved_at
                        else None
                    ),
                )
                for document in source_documents
            ],
            submissions=[
                SubmissionLineage(
                    id=submission.id,
                    assignment_id=submission.assignment_id,
                    learner_id=submission.learner_id,
                    policy_snapshot_id=submission.policy_snapshot_id,
                    version=submission.version,
                    review_state=submission.review_state,
                    redaction_status=submission.redaction_status,
                    approval_status=submission.approval_status,
                )
                for submission in submissions
            ],
            feedback_results=[
                FeedbackLineage(
                    id=result.id,
                    submission_id=result.submission_id,
                    submission_version=result.submission_version,
                    feedback_status=result.feedback_status,
                    validation_status=result.validation_status,
                    risk_flags=result.risk_flags,
                )
                for result in feedback_results
            ],
            approvals=approvals,
            reports=[
                ReportLineage(
                    id=report.id,
                    cohort_id=report.cohort_id,
                    version=report.version,
                    policy_snapshot_id=report.policy_snapshot_id,
                    created_by=report.created_by,
                    created_at=report.created_at.isoformat()
                    if report.created_at
                    else None,
                    risk_taxonomy_version=report.json_body.get(
                        "risk_taxonomy_version", RISK_TAXONOMY_VERSION
                    ),
                )
            ],
        )

    def _require_report(self, report_id: str, workspace_id: str) -> ProgressReport:
        report = self._session.scalar(
            select(ProgressReport).where(
                ProgressReport.id == report_id,
                ProgressReport.workspace_id == workspace_id,
            )
        )
        if report is None:
            raise ValueError("Report not found")
        return report

    def _require_cohort(self, cohort_id: str, workspace_id: str) -> Cohort:
        cohort = self._session.scalar(
            select(Cohort).where(
                Cohort.id == cohort_id,
                Cohort.workspace_id == workspace_id,
            )
        )
        if cohort is None:
            raise ValueError("Cohort not found")
        return cohort

    def _cohort_submissions(
        self, cohort_id: str, workspace_id: str
    ) -> list[Submission]:
        return self._session.scalars(
            select(Submission)
            .join(MissionAssignment, Submission.assignment_id == MissionAssignment.id)
            .where(
                MissionAssignment.cohort_id == cohort_id,
                MissionAssignment.workspace_id == workspace_id,
                Submission.workspace_id == workspace_id,
            )
            .order_by(Submission.id)
        ).all()

    def _feedback_results(
        self, submissions: list[Submission], workspace_id: str
    ) -> list[FeedbackResult]:
        if not submissions:
            return []
        submission_ids = [submission.id for submission in submissions]
        return self._session.scalars(
            select(FeedbackResult)
            .where(
                FeedbackResult.workspace_id == workspace_id,
                FeedbackResult.submission_id.in_(submission_ids),
            )
            .order_by(FeedbackResult.id)
        ).all()

    def _source_documents(
        self, submissions: list[Submission], workspace_id: str
    ) -> list[SourceDocument]:
        snapshot_ids = sorted(
            {submission.policy_snapshot_id for submission in submissions}
        )
        if not snapshot_ids:
            return []
        return self._session.scalars(
            select(SourceDocument)
            .where(
                SourceDocument.workspace_id == workspace_id,
                SourceDocument.snapshot_id.in_(snapshot_ids),
            )
            .order_by(SourceDocument.snapshot_id)
        ).all()


def _approval_lineage(
    source_documents: list[SourceDocument], submissions: list[Submission]
) -> list[ApprovalLineage]:
    document_approvals = [
        ApprovalLineage(
            ref=f"source_document:{document.id}",
            approval_type="source_document",
            subject_id=document.id,
            status=document.approval_status,
            actor_id=document.approved_by,
            approved_at=document.approved_at.isoformat()
            if document.approved_at
            else None,
        )
        for document in source_documents
    ]
    submission_approvals = [
        ApprovalLineage(
            ref=f"submission:{submission.id}",
            approval_type="submission",
            subject_id=submission.id,
            status=submission.approval_status,
            actor_id=submission.manager_id,
            approved_at=submission.approved_at.isoformat()
            if submission.approved_at
            else None,
        )
        for submission in submissions
    ]
    return sorted(
        [*document_approvals, *submission_approvals],
        key=lambda approval: approval.ref,
    )


def _controls(
    *,
    source_documents: list[SourceDocument],
    submissions: list[Submission],
    feedback_results: list[FeedbackResult],
    approvals: list[ApprovalLineage],
    report: ProgressReport,
) -> list[ControlMapping]:
    evidence = ControlEvidence(
        source_document_ids=[document.id for document in source_documents],
        submission_ids=[submission.id for submission in submissions],
        feedback_result_ids=[result.id for result in feedback_results],
        approval_refs=[approval.ref for approval in approvals],
        report_ids=[report.id],
    )
    return [
        ControlMapping(
            control_id="AI-GOV-001",
            title="Approved policy evidence is traceable",
            category="govern-map",
            evidence=evidence,
        ),
        ControlMapping(
            control_id="AI-GOV-002",
            title="Human approval decisions are attributable",
            category="govern",
            evidence=evidence,
        ),
        ControlMapping(
            control_id="AI-GOV-003",
            title="Manager reports retain evidence lineage",
            category="measure",
            evidence=evidence,
        ),
    ]
