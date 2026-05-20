from dataclasses import dataclass, field
from hashlib import sha256
from typing import Protocol

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from ai_rollout_os.audit.repository import AuditEventRepository
from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import Settings
from ai_rollout_os.db.models import User


class SSOConfigError(RuntimeError):
    pass


class SSOLoginError(ValueError):
    pass


@dataclass(frozen=True)
class OIDCProviderConfig:
    issuer_url: str
    client_id: str
    client_secret: str
    redirect_uri: str


@dataclass(frozen=True)
class OIDCClaims:
    issuer: str
    subject: str
    email: str
    email_verified: bool = True
    claims: dict[str, object] = field(default_factory=dict)


@dataclass(frozen=True)
class SSOLoginResult:
    token: str
    actor_id: str
    role: str
    workspace_id: str


class OIDCVerifier(Protocol):
    def verify_id_token(
        self, *, id_token: str, config: OIDCProviderConfig
    ) -> OIDCClaims:
        """Return provider-verified identity claims for an OIDC ID token."""


class SSOService:
    def __init__(
        self,
        *,
        session: Session,
        settings: Settings,
        verifier: OIDCVerifier,
    ) -> None:
        self._session = session
        self._settings = settings
        self._verifier = verifier

    def login_with_oidc_id_token(
        self, *, id_token: str, trace_id: str, ttl_seconds: int = 3600
    ) -> SSOLoginResult:
        config = oidc_provider_config(self._settings)
        claims = self._verifier.verify_id_token(id_token=id_token, config=config)
        if not claims.email_verified:
            self._audit_denied(claims, trace_id)
            raise SSOLoginError("SSO login failed")

        user = self._mapped_user(claims.email)
        if user is None:
            self._audit_denied(claims, trace_id)
            raise SSOLoginError("SSO login failed")

        self._audit_success(user, trace_id)
        token = create_token(
            actor_id=user.id,
            role=user.role,
            workspace_id=user.workspace_id,
            secret_key=self._settings.secret_key,
            ttl_seconds=ttl_seconds,
        )
        return SSOLoginResult(
            token=token,
            actor_id=user.id,
            role=user.role,
            workspace_id=user.workspace_id,
        )

    def _mapped_user(self, email: str) -> User | None:
        normalized_email = email.strip().lower()
        if not normalized_email:
            return None
        return self._session.scalar(
            select(User).where(func.lower(User.email) == normalized_email)
        )

    def _audit_success(self, user: User, trace_id: str) -> None:
        AuditEventRepository(self._session).append(
            actor_id=user.id,
            action="sso.login",
            resource_type="identity",
            resource_id=user.id,
            result="accepted",
            trace_id=trace_id,
        )

    def _audit_denied(self, claims: OIDCClaims, trace_id: str) -> None:
        AuditEventRepository(self._session).append(
            actor_id=None,
            action="sso.login",
            resource_type="identity",
            resource_id=opaque_identity_id(claims),
            result="denied",
            trace_id=trace_id,
        )


def oidc_provider_config(settings: Settings) -> OIDCProviderConfig:
    if not settings.sso_enabled:
        raise SSOConfigError("SSO is not enabled")
    required_values = {
        "OIDC_ISSUER_URL": settings.oidc_issuer_url,
        "OIDC_CLIENT_ID": settings.oidc_client_id,
        "OIDC_CLIENT_SECRET": settings.oidc_client_secret,
        "OIDC_REDIRECT_URI": settings.oidc_redirect_uri,
    }
    missing = [key for key, value in required_values.items() if not value]
    if missing:
        joined = ", ".join(sorted(missing))
        raise SSOConfigError(f"Missing required SSO environment variables: {joined}")
    return OIDCProviderConfig(
        issuer_url=str(settings.oidc_issuer_url),
        client_id=str(settings.oidc_client_id),
        client_secret=str(settings.oidc_client_secret),
        redirect_uri=str(settings.oidc_redirect_uri),
    )


def opaque_identity_id(claims: OIDCClaims) -> str:
    digest = sha256(f"{claims.issuer}|{claims.subject}".encode()).hexdigest()
    return digest[:24]
