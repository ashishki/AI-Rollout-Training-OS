import re
from pathlib import Path

WORKFLOW_PATH = Path(".github/workflows/ci.yml")


def read_workflow() -> str:
    return WORKFLOW_PATH.read_text()


def test_ci_workflow_has_required_steps() -> None:
    workflow = read_workflow()

    assert "uses: actions/checkout@9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0" in workflow
    assert (
        "uses: actions/setup-python@ece7cb06caefa5fff74198d8649806c4678c61a1"
        in workflow
    )
    assert (
        "uses: actions/setup-node@a0853c24544627f65ddf259abe73b1d18a591444" in workflow
    )
    assert 'python-version: "3.12"' in workflow
    assert 'node-version: "22"' in workflow
    assert "pip install -r requirements-dev.txt -e ." in workflow
    assert "npm ci" in workflow
    assert "npm audit --audit-level=high" in workflow
    assert "npm run build" in workflow
    assert "ruff check scripts ai_rollout_os frontend tests migrations" in workflow
    assert (
        "ruff format --check scripts ai_rollout_os frontend tests migrations"
        in workflow
    )
    assert "python -m pytest tests/ -q --tb=short" in workflow
    assert "python scripts/eval.py --no-write" in workflow


def test_ci_actions_are_pinned_read_only_and_do_not_persist_credentials() -> None:
    workflow = read_workflow()
    official_action_revisions = re.findall(
        r"uses: (actions/[^@\s]+)@([^\s]+)", workflow
    )

    assert official_action_revisions == [
        ("actions/checkout", "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0"),
        ("actions/setup-python", "ece7cb06caefa5fff74198d8649806c4678c61a1"),
        ("actions/setup-node", "a0853c24544627f65ddf259abe73b1d18a591444"),
    ]
    assert workflow.count("permissions:\n  contents: read") == 1
    assert "permissions: write" not in workflow
    assert workflow.count("persist-credentials: false") == 1
    checkout_step = workflow.split("uses: actions/checkout@", maxsplit=1)[1].split(
        "\n\n", maxsplit=1
    )[0]
    assert "persist-credentials: false" in checkout_step


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
