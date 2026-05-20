import os
from collections.abc import Mapping
from dataclasses import dataclass


class ConfigError(RuntimeError):
    """Raised when runtime configuration is incomplete or invalid."""


REQUIRED_RUNTIME_VARS = (
    "APP_ENV",
    "DATABASE_URL",
    "SECRET_KEY",
    "AI_PROVIDER_API_KEY",
    "MODEL_FAST",
    "MODEL_STRONG",
    "EMBEDDING_MODEL",
)

TEST_DEFAULTS = {
    "APP_ENV": "test",
    "DATABASE_URL": "postgresql+psycopg://testuser:testpassword@localhost:5432/testdb",
    "SECRET_KEY": "test-secret-key",
    "AI_PROVIDER_API_KEY": "test-key",
    "MODEL_FAST": "test-fast-model",
    "MODEL_STRONG": "test-strong-model",
    "EMBEDDING_MODEL": "test-embedding-model",
    "INDEX_MAX_AGE_DAYS": "7",
    "FEEDBACK_TIMEOUT_SECONDS": "60",
    "REMINDER_WINDOW_DAYS": "3",
    "REMINDER_DELIVERY_ENABLED": "false",
    "RETENTION_DAYS": "365",
    "SSO_ENABLED": "false",
}


@dataclass(frozen=True)
class Settings:
    service_name: str = "ai-rollout-training-os"
    app_env: str = "test"
    database_url: str = TEST_DEFAULTS["DATABASE_URL"]
    secret_key: str = TEST_DEFAULTS["SECRET_KEY"]
    ai_provider_api_key: str = TEST_DEFAULTS["AI_PROVIDER_API_KEY"]
    model_fast: str = TEST_DEFAULTS["MODEL_FAST"]
    model_strong: str = TEST_DEFAULTS["MODEL_STRONG"]
    embedding_model: str = TEST_DEFAULTS["EMBEDDING_MODEL"]
    index_max_age_days: int = 7
    feedback_timeout_seconds: int = 60
    reminder_window_days: int = 3
    reminder_delivery_enabled: bool = False
    retention_days: int = 365
    sso_enabled: bool = False
    oidc_issuer_url: str | None = None
    oidc_client_id: str | None = None
    oidc_client_secret: str | None = None
    oidc_redirect_uri: str | None = None


def get_settings(environ: Mapping[str, str] | None = None) -> Settings:
    source = os.environ if environ is None else environ
    app_env = source.get("APP_ENV", TEST_DEFAULTS["APP_ENV"])
    values = {key: source.get(key) for key in REQUIRED_RUNTIME_VARS}

    if app_env == "test":
        values = {
            key: values[key] or TEST_DEFAULTS[key] for key in REQUIRED_RUNTIME_VARS
        }
    else:
        missing = [key for key, value in values.items() if not value]
        if missing:
            joined = ", ".join(sorted(missing))
            raise ConfigError(f"Missing required environment variables: {joined}")

    sso_enabled = _bool_env(source.get("SSO_ENABLED", TEST_DEFAULTS["SSO_ENABLED"]))
    oidc_values = {
        "OIDC_ISSUER_URL": source.get("OIDC_ISSUER_URL"),
        "OIDC_CLIENT_ID": source.get("OIDC_CLIENT_ID"),
        "OIDC_CLIENT_SECRET": source.get("OIDC_CLIENT_SECRET"),
        "OIDC_REDIRECT_URI": source.get("OIDC_REDIRECT_URI"),
    }
    if sso_enabled:
        missing_oidc = [key for key, value in oidc_values.items() if not value]
        if missing_oidc:
            joined = ", ".join(sorted(missing_oidc))
            raise ConfigError(f"Missing required SSO environment variables: {joined}")

    return Settings(
        app_env=app_env,
        database_url=values["DATABASE_URL"] or TEST_DEFAULTS["DATABASE_URL"],
        secret_key=values["SECRET_KEY"] or TEST_DEFAULTS["SECRET_KEY"],
        ai_provider_api_key=values["AI_PROVIDER_API_KEY"]
        or TEST_DEFAULTS["AI_PROVIDER_API_KEY"],
        model_fast=values["MODEL_FAST"] or TEST_DEFAULTS["MODEL_FAST"],
        model_strong=values["MODEL_STRONG"] or TEST_DEFAULTS["MODEL_STRONG"],
        embedding_model=values["EMBEDDING_MODEL"] or TEST_DEFAULTS["EMBEDDING_MODEL"],
        index_max_age_days=int(source.get("INDEX_MAX_AGE_DAYS", "7")),
        feedback_timeout_seconds=int(source.get("FEEDBACK_TIMEOUT_SECONDS", "60")),
        reminder_window_days=int(source.get("REMINDER_WINDOW_DAYS", "3")),
        reminder_delivery_enabled=_bool_env(
            source.get("REMINDER_DELIVERY_ENABLED", "false")
        ),
        retention_days=int(source.get("RETENTION_DAYS", "365")),
        sso_enabled=sso_enabled,
        oidc_issuer_url=oidc_values["OIDC_ISSUER_URL"],
        oidc_client_id=oidc_values["OIDC_CLIENT_ID"],
        oidc_client_secret=oidc_values["OIDC_CLIENT_SECRET"],
        oidc_redirect_uri=oidc_values["OIDC_REDIRECT_URI"],
    )


def _bool_env(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "on"}
