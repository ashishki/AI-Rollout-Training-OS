from collections.abc import Callable
from dataclasses import dataclass

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session, sessionmaker

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.dependencies import authenticate_request
from ai_rollout_os.auth.tokens import ActorContext

AUTHENTICATED_ACTOR = Depends(authenticate_request)


@dataclass(frozen=True)
class Permission:
    name: str
    allowed_roles: frozenset[str]
    description: str


PERMISSIONS = {
    "app.shell.view": Permission(
        "app.shell.view",
        frozenset({"operator", "manager", "learner"}),
        "View the authenticated application shell.",
    ),
    "app.operator.view": Permission(
        "app.operator.view", frozenset({"operator"}), "View operator UI sections."
    ),
    "app.learner.view": Permission(
        "app.learner.view", frozenset({"learner"}), "View learner UI sections."
    ),
    "app.manager.view": Permission(
        "app.manager.view", frozenset({"manager"}), "View manager UI sections."
    ),
    "app.operator.documents.create": Permission(
        "app.operator.documents.create",
        frozenset({"operator"}),
        "Create policy and SOP documents from the operator UI.",
    ),
    "app.operator.guardrail_quizzes.create": Permission(
        "app.operator.guardrail_quizzes.create",
        frozenset({"operator"}),
        "Create guardrail quizzes from the operator UI.",
    ),
    "app.operator.role_packs.create": Permission(
        "app.operator.role_packs.create",
        frozenset({"operator"}),
        "Create role packs from the operator UI.",
    ),
    "app.operator.missions.create": Permission(
        "app.operator.missions.create",
        frozenset({"operator"}),
        "Create missions from the operator UI.",
    ),
    "app.operator.role_packs.launch": Permission(
        "app.operator.role_packs.launch",
        frozenset({"operator"}),
        "Launch role packs from the operator UI.",
    ),
    "app.operator.cohorts.create": Permission(
        "app.operator.cohorts.create",
        frozenset({"operator"}),
        "Create cohorts from the operator UI.",
    ),
    "app.operator.cohorts.launch": Permission(
        "app.operator.cohorts.launch",
        frozenset({"operator"}),
        "Launch cohorts from the operator UI.",
    ),
    "app.learner.guardrail_submissions.create": Permission(
        "app.learner.guardrail_submissions.create",
        frozenset({"learner"}),
        "Submit guardrail quiz answers from the learner UI.",
    ),
    "app.learner.submissions.create": Permission(
        "app.learner.submissions.create",
        frozenset({"learner"}),
        "Submit mission artifacts from the learner UI.",
    ),
    "app.manager.submissions.approve": Permission(
        "app.manager.submissions.approve",
        frozenset({"manager"}),
        "Approve workflow changes from the manager UI.",
    ),
    "app.manager.reports.create": Permission(
        "app.manager.reports.create",
        frozenset({"manager"}),
        "Create progress reports from the manager UI.",
    ),
    "documents.create": Permission(
        "documents.create", frozenset({"operator"}), "Create source documents."
    ),
    "documents.update": Permission(
        "documents.update", frozenset({"operator"}), "Update source documents."
    ),
    "documents.read_snapshot": Permission(
        "documents.read_snapshot",
        frozenset({"operator"}),
        "Read source document snapshots.",
    ),
    "documents.approve": Permission(
        "documents.approve",
        frozenset({"operator", "manager"}),
        "Approve policy and SOP document snapshots for retrieval.",
    ),
    "role_packs.create": Permission(
        "role_packs.create", frozenset({"operator"}), "Create draft role packs."
    ),
    "role_packs.missions.create": Permission(
        "role_packs.missions.create",
        frozenset({"operator"}),
        "Add missions to role packs.",
    ),
    "role_packs.launch": Permission(
        "role_packs.launch", frozenset({"operator"}), "Launch role packs."
    ),
    "role_packs.versions.create": Permission(
        "role_packs.versions.create",
        frozenset({"operator"}),
        "Create role-pack versions.",
    ),
    "role_packs.versions.compare": Permission(
        "role_packs.versions.compare",
        frozenset({"operator"}),
        "Compare role-pack versions.",
    ),
    "cohorts.create": Permission(
        "cohorts.create", frozenset({"operator"}), "Create cohorts."
    ),
    "cohorts.launch": Permission(
        "cohorts.launch", frozenset({"operator"}), "Launch cohorts."
    ),
    "cohorts.assignments.read": Permission(
        "cohorts.assignments.read",
        frozenset({"learner"}),
        "Read learner cohort assignments.",
    ),
    "guardrails.create": Permission(
        "guardrails.create", frozenset({"operator"}), "Create guardrail quizzes."
    ),
    "guardrails.submissions.create": Permission(
        "guardrails.submissions.create",
        frozenset({"learner"}),
        "Submit guardrail quiz answers.",
    ),
    "guardrails.feedback_release.read": Permission(
        "guardrails.feedback_release.read",
        frozenset({"learner"}),
        "Read guardrail feedback release status.",
    ),
    "submissions.create": Permission(
        "submissions.create", frozenset({"learner"}), "Create mission submissions."
    ),
    "submissions.redaction_approval.create": Permission(
        "submissions.redaction_approval.create",
        frozenset({"manager"}),
        "Approve flagged submissions for feedback.",
    ),
    "manager.submissions.read": Permission(
        "manager.submissions.read",
        frozenset({"manager"}),
        "Read manager submission review queue.",
    ),
    "manager.submissions.approve": Permission(
        "manager.submissions.approve",
        frozenset({"manager"}),
        "Approve manager-reviewed workflow changes.",
    ),
    "manager.dashboard.read": Permission(
        "manager.dashboard.read", frozenset({"manager"}), "Read manager dashboard."
    ),
    "manager.reports.create": Permission(
        "manager.reports.create", frozenset({"manager"}), "Create progress reports."
    ),
}


ROUTE_PERMISSIONS = {
    ("GET", "/app"): "app.shell.view",
    ("GET", "/app/permission-simulator"): "app.shell.view",
    ("POST", "/app/permission-simulator/decisions"): "app.shell.view",
    ("GET", "/app/operator/{section}"): "app.operator.view",
    ("GET", "/app/learner/{section}"): "app.learner.view",
    ("GET", "/app/manager/{section}"): "app.manager.view",
    ("POST", "/app/operator/documents"): "app.operator.documents.create",
    ("POST", "/app/operator/guardrail-quizzes"): (
        "app.operator.guardrail_quizzes.create"
    ),
    ("POST", "/app/operator/role-packs"): "app.operator.role_packs.create",
    ("POST", "/app/operator/missions"): "app.operator.missions.create",
    ("POST", "/app/operator/role-packs/launch"): "app.operator.role_packs.launch",
    ("POST", "/app/operator/cohorts"): "app.operator.cohorts.create",
    ("POST", "/app/operator/cohorts/launch"): "app.operator.cohorts.launch",
    ("POST", "/app/learner/guardrail-submissions"): (
        "app.learner.guardrail_submissions.create"
    ),
    ("POST", "/app/learner/submissions"): "app.learner.submissions.create",
    ("POST", "/app/manager/submissions/approve"): "app.manager.submissions.approve",
    ("POST", "/app/manager/reports"): "app.manager.reports.create",
    ("POST", "/documents"): "documents.create",
    ("PUT", "/documents/{logical_document_id}"): "documents.update",
    ("GET", "/documents/{logical_document_id}/snapshots/{snapshot_id}"): (
        "documents.read_snapshot"
    ),
    ("POST", "/documents/{logical_document_id}/snapshots/{snapshot_id}/approval"): (
        "documents.approve"
    ),
    ("POST", "/role-packs"): "role_packs.create",
    ("POST", "/role-packs/{role_pack_id}/missions"): "role_packs.missions.create",
    ("POST", "/role-packs/{role_pack_id}/launch"): "role_packs.launch",
    ("POST", "/role-packs/{role_pack_id}/versions"): "role_packs.versions.create",
    ("GET", "/role-packs/{role_pack_id}/versions/compare"): (
        "role_packs.versions.compare"
    ),
    ("POST", "/cohorts"): "cohorts.create",
    ("POST", "/cohorts/{cohort_id}/launch"): "cohorts.launch",
    ("GET", "/cohorts/{cohort_id}/assignments"): "cohorts.assignments.read",
    ("POST", "/guardrail-quizzes"): "guardrails.create",
    ("POST", "/guardrail-quizzes/{quiz_id}/submissions"): (
        "guardrails.submissions.create"
    ),
    ("GET", "/missions/{mission_id}/feedback-release"): (
        "guardrails.feedback_release.read"
    ),
    ("POST", "/missions/{mission_id}/submissions"): "submissions.create",
    ("POST", "/submissions/{submission_id}/redaction-approval"): (
        "submissions.redaction_approval.create"
    ),
    ("GET", "/manager/submissions"): "manager.submissions.read",
    ("POST", "/manager/submissions/{submission_id}/approve"): (
        "manager.submissions.approve"
    ),
    ("GET", "/manager/cohorts/{cohort_id}/dashboard"): "manager.dashboard.read",
    ("POST", "/manager/cohorts/{cohort_id}/reports"): "manager.reports.create",
}


def require_permission(permission_name: str) -> Callable[..., ActorContext]:
    if permission_name not in PERMISSIONS:
        raise ValueError(f"Unknown permission: {permission_name}")
    permission = PERMISSIONS[permission_name]

    def dependency(
        request: Request,
        actor: ActorContext = AUTHENTICATED_ACTOR,
    ) -> ActorContext:
        if actor.role not in permission.allowed_roles:
            audit_denied_access(
                request=request,
                actor=actor,
                resource_type="permission",
                resource_id=permission.name,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return actor

    dependency.permission_name = permission_name  # type: ignore[attr-defined]
    return dependency


def require_role(*allowed_roles: str) -> Callable[..., ActorContext]:
    def dependency(
        request: Request,
        actor: ActorContext = AUTHENTICATED_ACTOR,
    ) -> ActorContext:
        if actor.role not in allowed_roles:
            audit_denied_access(
                request=request,
                actor=actor,
                resource_type="route",
                resource_id=request.url.path,
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return actor

    return dependency


def require_workspace_match(
    path_param: str = "workspace_id",
) -> Callable[..., ActorContext]:
    def dependency(
        request: Request,
        actor: ActorContext = AUTHENTICATED_ACTOR,
    ) -> ActorContext:
        requested_workspace_id = request.path_params.get(path_param)
        if requested_workspace_id != actor.workspace_id:
            audit_denied_access(
                request=request,
                actor=actor,
                resource_type="workspace",
                resource_id=str(requested_workspace_id),
            )
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="Access denied"
            )
        return actor

    return dependency


def audit_denied_access(
    *,
    request: Request,
    actor: ActorContext,
    resource_type: str,
    resource_id: str,
) -> None:
    session_factory: sessionmaker[Session] | None = getattr(
        request.app.state, "session_factory", None
    )
    if session_factory is None:
        return

    with session_factory() as session:
        AuditEventRepository(session).append(
            actor_id=actor.actor_id,
            action="denied_access",
            resource_type=resource_type,
            resource_id=resource_id,
            result="denied",
            trace_id=actor.trace_id,
        )
        session.commit()
