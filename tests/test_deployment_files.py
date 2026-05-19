from pathlib import Path


def test_docker_compose_config_contains_required_services() -> None:
    compose = Path("docker-compose.yml").read_text()

    assert "services:" in compose
    assert "postgres:" in compose
    assert "web:" in compose
    assert "worker:" in compose
    assert "migrate:" in compose
    assert "pgvector/pgvector:pg16" in compose
    assert '["alembic", "upgrade", "head"]' in compose
    for variable in [
        "APP_ENV",
        "DATABASE_URL",
        "SECRET_KEY",
        "AI_PROVIDER_API_KEY",
        "MODEL_FAST",
        "MODEL_STRONG",
        "EMBEDDING_MODEL",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
    ]:
        assert variable in compose


def test_worker_uses_same_image_and_bounded_command() -> None:
    compose = Path("docker-compose.yml").read_text()

    assert compose.count("image: ai-rollout-training-os:${IMAGE_TAG:-local}") >= 3
    assert '["python", "-m", "ai_rollout_os.jobs.runner", "--run-once"]' in compose
    assert "--privileged" not in compose
    assert "docker.sock" not in compose


def test_deployment_files_have_no_real_secrets() -> None:
    combined = "\n".join(
        [
            Path("Dockerfile").read_text(),
            Path("docker-compose.yml").read_text(),
            Path(".env.example").read_text(),
        ]
    )

    forbidden = ["sk-", "prod_", "live-secret", "real-api-key", "password123"]
    for fragment in forbidden:
        assert fragment not in combined

    assert "replace-with-provider-api-key" in combined
    assert "replace-with-random-32-byte-secret" in combined
    assert ".env" in combined
