from uuid import uuid4

from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import (
    Cohort,
    FeedbackResult,
    MissionAssignment,
    ProgressReport,
    Submission,
)
from ai_rollout_os.reporting.dashboard import DashboardService


class ReportRead(BaseModel):
    id: str
    cohort_id: str
    version: int
    role_pack_version: int
    policy_snapshot_id: str
    dashboard_metrics: dict
    markdown_body: str
    json_body: dict


class ReportService:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create_report(self, *, cohort_id: str, actor: ActorContext) -> ProgressReport:
        cohort = self._require_cohort(cohort_id, actor.workspace_id)
        metrics = DashboardService(self._session).cohort_dashboard(
            cohort_id=cohort.id,
            workspace_id=actor.workspace_id,
        )
        submissions = self._cohort_submissions(cohort.id, actor.workspace_id)
        policy_snapshot_id = _policy_snapshot_id(submissions)
        approved_changes = [
            submission.approved_workflow_change
            for submission in submissions
            if submission.approval_status == "approved"
            and submission.approved_workflow_change
        ]
        open_risks = self._risk_flags(submissions)
        next_version = self._next_report_version(cohort.id, actor.workspace_id)
        json_body = {
            "cohort": {
                "id": cohort.id,
                "role_pack_id": cohort.role_pack_id,
                "role_pack_version": cohort.role_pack_version,
                "policy_snapshot_id": policy_snapshot_id,
            },
            "dashboard_metrics": metrics.model_dump(),
            "approved_workflow_changes": approved_changes,
            "open_risk_flags": open_risks,
        }
        report = ProgressReport(
            id=f"report_{uuid4().hex}",
            workspace_id=actor.workspace_id,
            cohort_id=cohort.id,
            version=next_version,
            role_pack_version=cohort.role_pack_version,
            policy_snapshot_id=policy_snapshot_id,
            dashboard_metrics=metrics.model_dump(),
            markdown_body=_markdown_report(json_body),
            json_body=json_body,
            created_by=actor.actor_id,
        )
        self._session.add(report)
        self._session.flush()
        AuditEventRepository(self._session).append(
            actor_id=actor.actor_id,
            action="report.created",
            resource_type="progress_report",
            resource_id=report.id,
            result="success",
            trace_id=actor.trace_id,
        )
        self._session.flush()
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
        ).all()

    def _risk_flags(self, submissions: list[Submission]) -> list[str]:
        if not submissions:
            return []
        submission_ids = [submission.id for submission in submissions]
        results = self._session.scalars(
            select(FeedbackResult).where(
                FeedbackResult.submission_id.in_(submission_ids)
            )
        ).all()
        return sorted({flag for result in results for flag in result.risk_flags})

    def _next_report_version(self, cohort_id: str, workspace_id: str) -> int:
        current = self._session.scalar(
            select(func.max(ProgressReport.version)).where(
                ProgressReport.cohort_id == cohort_id,
                ProgressReport.workspace_id == workspace_id,
            )
        )
        return int(current or 0) + 1


def report_read(report: ProgressReport) -> ReportRead:
    return ReportRead(
        id=report.id,
        cohort_id=report.cohort_id,
        version=report.version,
        role_pack_version=report.role_pack_version,
        policy_snapshot_id=report.policy_snapshot_id,
        dashboard_metrics=report.dashboard_metrics,
        markdown_body=report.markdown_body,
        json_body=report.json_body,
    )


def _policy_snapshot_id(submissions: list[Submission]) -> str:
    snapshot_ids = sorted({submission.policy_snapshot_id for submission in submissions})
    return snapshot_ids[0] if snapshot_ids else "none"


def _markdown_report(report: dict) -> str:
    metrics = report["dashboard_metrics"]
    approved_changes = report["approved_workflow_changes"]
    open_risks = report["open_risk_flags"]
    lines = [
        f"# Progress Report: {report['cohort']['id']}",
        "",
        f"- Role pack version: {report['cohort']['role_pack_version']}",
        f"- Policy snapshot: {report['cohort']['policy_snapshot_id']}",
        f"- Completion rate: {metrics['completion_rate']}",
        f"- Submission rate: {metrics['submission_rate']}",
        f"- Guardrail pass rate: {metrics['guardrail_pass_rate']}",
        f"- Approved workflow count: {metrics['approved_workflow_count']}",
        "",
        "## Approved Workflow Changes",
    ]
    lines.extend(f"- {change}" for change in approved_changes)
    if not approved_changes:
        lines.append("- none")
    lines.extend(["", "## Open Risk Flags"])
    lines.extend(f"- {risk}" for risk in open_risks)
    if not open_risks:
        lines.append("- none")
    return "\n".join(lines)
