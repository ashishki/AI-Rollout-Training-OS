from pathlib import Path

WORKFLOW_PATH = Path(".github/workflows/ci.yml")


def read_workflow() -> str:
    return WORKFLOW_PATH.read_text()


def test_ci_workflow_has_required_steps() -> None:
    workflow = read_workflow()

    assert "uses: actions/checkout@v4" in workflow
    assert "uses: actions/setup-python@v5" in workflow
    assert 'python-version: "3.12"' in workflow
    assert "pip install -r requirements-dev.txt -e ." in workflow
    assert "ruff check scripts ai_rollout_os frontend tests migrations" in workflow
    assert (
        "ruff format --check scripts ai_rollout_os frontend tests migrations"
        in workflow
    )
    assert "python -m pytest tests/ -q --tb=short" in workflow
    assert "python scripts/eval.py --no-write" in workflow


def test_ci_workflow_declares_pgvector_service() -> None:
    workflow = read_workflow()

    assert "services:" in workflow
    assert "postgres:" in workflow
    assert "image: pgvector/pgvector:pg16" in workflow
    assert "POSTGRES_USER: testuser" in workflow
    assert "POSTGRES_PASSWORD: testpassword" in workflow
    assert "POSTGRES_DB: testdb" in workflow
    assert (
        "DATABASE_URL: postgresql+psycopg://testuser:testpassword@localhost:5432/testdb"
    ) in workflow


def test_ci_workflow_has_no_production_secrets() -> None:
    workflow = read_workflow()
    forbidden_fragments = [
        "sk-",
        "prod_",
        "production-password",
        "live-secret",
        "real-api-key",
    ]

    for fragment in forbidden_fragments:
        assert fragment not in workflow

    assert "AI_PROVIDER_API_KEY: test-key" in workflow
    assert "SECRET_KEY: test-secret-key" in workflow
