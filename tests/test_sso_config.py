from pathlib import Path

import pytest
from ai_rollout_os.core.config import ConfigError, get_settings


def test_sso_secrets_are_env_only() -> None:
    env = required_production_env()
    env.update(
        {
            "SSO_ENABLED": "true",
            "OIDC_ISSUER_URL": "https://idp.example.test",
            "OIDC_CLIENT_ID": "enterprise-client-id",
            "OIDC_CLIENT_SECRET": "actual-oidc-secret-value",
            "OIDC_REDIRECT_URI": "https://app.example.test/auth/oidc/callback",
        }
    )

    settings = get_settings(env)

    assert settings.sso_enabled is True
    assert settings.oidc_client_secret == "actual-oidc-secret-value"
    for path in (Path(".env.example"), Path("docs/security_review.md")):
        text = path.read_text()
        assert "OIDC_CLIENT_SECRET" in text
        assert "actual-oidc-secret-value" not in text


def test_sso_enabled_requires_oidc_env_without_leaking_values() -> None:
    env = required_production_env()
    env.update(
        {
            "SSO_ENABLED": "true",
            "OIDC_ISSUER_URL": "https://idp.example.test",
            "OIDC_CLIENT_SECRET": "actual-oidc-secret-value",
        }
    )

    with pytest.raises(ConfigError) as exc_info:
        get_settings(env)

    message = str(exc_info.value)
    assert "OIDC_CLIENT_ID" in message
    assert "OIDC_REDIRECT_URI" in message
    assert "actual-oidc-secret-value" not in message


def required_production_env() -> dict[str, str]:
    return {
        "APP_ENV": "production",
        "DATABASE_URL": "postgresql+psycopg://user:password@db:5432/app",
        "SECRET_KEY": "production-secret-key",
        "AI_PROVIDER_API_KEY": "provider-key",
        "MODEL_FAST": "fast-model",
        "MODEL_STRONG": "strong-model",
        "EMBEDDING_MODEL": "embedding-model",
    }
