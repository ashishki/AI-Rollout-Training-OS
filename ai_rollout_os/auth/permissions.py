from collections.abc import Callable

from fastapi import Depends, HTTPException, Request, status
from sqlalchemy.orm import Session, sessionmaker

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.dependencies import authenticate_request
from ai_rollout_os.auth.tokens import ActorContext

AUTHENTICATED_ACTOR = Depends(authenticate_request)


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
