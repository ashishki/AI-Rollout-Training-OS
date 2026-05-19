import pytest
from ai_rollout_os.core.config import ConfigError, get_settings


def test_missing_required_env_reports_names_only() -> None:
    env = {
        "APP_ENV": "production",
        "SECRET_KEY": "actual-secret-value",
    }

    with pytest.raises(ConfigError) as exc_info:
        get_settings(env)

    message = str(exc_info.value)
    assert "DATABASE_URL" in message
    assert "AI_PROVIDER_API_KEY" in message
    assert "MODEL_FAST" in message
    assert "actual-secret-value" not in message
    assert "test-key" not in message
