from pathlib import Path


def test_pilot_readiness_doc_contains_required_sections() -> None:
    doc = Path("docs/pilot_readiness.md").read_text()

    for heading in [
        "## Required Env Vars",
        "## Operator Setup Steps",
        "## Known Non-Goals",
        "## Go/No-Go Checks",
    ]:
        assert heading in doc

    for env_var in [
        "APP_ENV",
        "DATABASE_URL",
        "SECRET_KEY",
        "AI_PROVIDER_API_KEY",
        "MODEL_FAST",
        "MODEL_STRONG",
        "EMBEDDING_MODEL",
    ]:
        assert f"`{env_var}`" in doc

    assert "not a production certification gate" in doc
    assert "No autonomous agent loop" in doc
