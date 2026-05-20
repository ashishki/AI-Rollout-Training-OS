from ai_rollout_os.auth.sso import OIDCClaims, OIDCProviderConfig, SSOService
from ai_rollout_os.auth.tokens import decode_token
from ai_rollout_os.core.config import Settings, get_settings
from ai_rollout_os.db.models import AuditEvent, User, Workspace
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_oidc_login_maps_roles_server_side(migrated_engine: Engine) -> None:
    settings = sso_settings()
    with Session(migrated_engine) as session:
        session.add(Workspace(id="ws-1", name="Pilot Workspace"))
        session.add(
            User(
                id="learner-1",
                workspace_id="ws-1",
                email="learner@example.com",
                role="learner",
            )
        )
        session.commit()

        result = SSOService(
            session=session,
            settings=settings,
            verifier=FakeOIDCVerifier(
                OIDCClaims(
                    issuer=settings.oidc_issuer_url or "",
                    subject="provider-user-123",
                    email="LEARNER@example.com",
                    claims={"role": "operator", "workspace_id": "attacker-ws"},
                )
            ),
        ).login_with_oidc_id_token(
            id_token="provider-issued-id-token",
            trace_id="trace-sso",
            ttl_seconds=60,
        )
        session.commit()

    payload = decode_token(result.token, secret_key=settings.secret_key)
    assert result.actor_id == "learner-1"
    assert result.role == "learner"
    assert result.workspace_id == "ws-1"
    assert payload["role"] == "learner"
    assert payload["workspace_id"] == "ws-1"

    with Session(migrated_engine) as session:
        events = session.scalars(select(AuditEvent).order_by(AuditEvent.id)).all()
    assert [(event.action, event.resource_id, event.result) for event in events] == [
        ("sso.login", "learner-1", "accepted")
    ]


class FakeOIDCVerifier:
    def __init__(self, claims: OIDCClaims) -> None:
        self._claims = claims
        self.seen_config: OIDCProviderConfig | None = None

    def verify_id_token(
        self, *, id_token: str, config: OIDCProviderConfig
    ) -> OIDCClaims:
        assert id_token == "provider-issued-id-token"
        assert config.client_secret == "test-oidc-client-secret"
        self.seen_config = config
        return self._claims


def sso_settings() -> Settings:
    return get_settings(
        {
            "APP_ENV": "test",
            "SSO_ENABLED": "true",
            "OIDC_ISSUER_URL": "https://idp.example.test",
            "OIDC_CLIENT_ID": "test-client-id",
            "OIDC_CLIENT_SECRET": "test-oidc-client-secret",
            "OIDC_REDIRECT_URI": "https://app.example.test/auth/oidc/callback",
        }
    )
