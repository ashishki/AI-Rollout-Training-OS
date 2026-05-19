from uuid import uuid4

from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from ai_rollout_os.auth.tokens import ActorContext, TokenError, decode_token
from ai_rollout_os.core.config import Settings
from ai_rollout_os.observability.tracing import set_trace_id

bearer_scheme = HTTPBearer(auto_error=False)


def get_settings_from_app(request: Request) -> Settings:
    return request.app.state.settings


AUTH_CREDENTIALS = Depends(bearer_scheme)
APP_SETTINGS = Depends(get_settings_from_app)


def authenticate_request(
    request: Request,
    credentials: HTTPAuthorizationCredentials | None = AUTH_CREDENTIALS,
    settings: Settings = APP_SETTINGS,
) -> ActorContext:
    if credentials is None or credentials.scheme.lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication required"
        )

    try:
        payload = decode_token(credentials.credentials, secret_key=settings.secret_key)
    except (TokenError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
        ) from None

    trace_id = request.headers.get("x-trace-id") or uuid4().hex
    set_trace_id(trace_id)
    actor = ActorContext(
        actor_id=str(payload["actor_id"]),
        role=str(payload["role"]),
        workspace_id=str(payload["workspace_id"]),
        trace_id=trace_id,
    )
    request.state.actor_id = actor.actor_id
    request.state.role = actor.role
    request.state.workspace_id = actor.workspace_id
    request.state.trace_id = actor.trace_id
    request.state.actor_context = actor
    return actor
