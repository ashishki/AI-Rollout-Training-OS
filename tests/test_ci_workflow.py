from copy import deepcopy
from pathlib import Path

import pytest
import yaml

WORKFLOW_PATH = Path(".github/workflows/ci.yml")
WORKFLOW_PATHS = tuple(sorted(Path(".github/workflows").glob("*.y*ml")))
PINNED_OFFICIAL_ACTIONS = {
    "actions/checkout": "9c091bb21b7c1c1d1991bb908d89e4e9dddfe3e0",
    "actions/setup-python": "ece7cb06caefa5fff74198d8649806c4678c61a1",
    "actions/setup-node": "a0853c24544627f65ddf259abe73b1d18a591444",
}


def read_workflow() -> str:
    return WORKFLOW_PATH.read_text()


def iter_uses_nodes(value: object):
    if isinstance(value, dict):
        if isinstance(value.get("uses"), str):
            yield value
        for child in value.values():
            yield from iter_uses_nodes(child)
    elif isinstance(value, list):
        for child in value:
            yield from iter_uses_nodes(child)


def assert_workflow_security(workflow: dict) -> int:
    assert workflow["permissions"] == {"contents": "read"}
    assert all("permissions" not in job for job in workflow["jobs"].values())

    action_nodes = list(iter_uses_nodes(workflow))
    assert action_nodes
    for node in action_nodes:
        action, separator, revision = node["uses"].partition("@")
        assert separator == "@"
        assert action in PINNED_OFFICIAL_ACTIONS
        assert revision == PINNED_OFFICIAL_ACTIONS[action]
        if action == "actions/checkout":
            assert node.get("with", {}).get("persist-credentials") is False
    return len(action_nodes)


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
    action_count = 0

    assert WORKFLOW_PATHS
    for workflow_path in WORKFLOW_PATHS:
        workflow = yaml.safe_load(workflow_path.read_text(encoding="utf-8"))
        action_count += assert_workflow_security(workflow)

    assert action_count == 3


@pytest.mark.parametrize(
    "mutation",
    (
        "mutable_pin",
        "broad_top_level",
        "job_override",
        "persist_missing",
        "persist_true",
        "unapproved_action",
    ),
)
def test_ci_security_guard_rejects_unsafe_mutations(mutation: str) -> None:
    workflow = yaml.safe_load(WORKFLOW_PATH.read_text(encoding="utf-8"))
    mutated = deepcopy(workflow)
    action_nodes = list(iter_uses_nodes(mutated))
    checkout = next(
        node for node in action_nodes if node["uses"].startswith("actions/checkout@")
    )

    if mutation == "mutable_pin":
        checkout["uses"] = "actions/checkout@v7"
    elif mutation == "broad_top_level":
        mutated["permissions"] = {"contents": "write"}
    elif mutation == "job_override":
        next(iter(mutated["jobs"].values()))["permissions"] = {"contents": "write"}
    elif mutation == "persist_missing":
        checkout["with"].pop("persist-credentials")
    elif mutation == "persist_true":
        checkout["with"]["persist-credentials"] = True
    else:
        next(iter(mutated["jobs"].values()))["steps"].append(
            {"uses": "untrusted/example@0123456789abcdef"}
        )

    with pytest.raises(AssertionError):
        assert_workflow_security(mutated)


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
