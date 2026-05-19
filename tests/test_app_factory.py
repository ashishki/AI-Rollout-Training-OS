from ai_rollout_os.main import create_app
from fastapi import FastAPI


def test_create_app_without_external_resources(monkeypatch) -> None:
    monkeypatch.delenv("AI_PROVIDER_API_KEY", raising=False)
    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.delenv("SECRET_KEY", raising=False)

    app = create_app()

    assert isinstance(app, FastAPI)
    assert app.state.settings.service_name == "ai-rollout-training-os"
