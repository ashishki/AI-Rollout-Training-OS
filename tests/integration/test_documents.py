import logging

from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.db.models import SourceDocument
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker


def test_create_policy_document_snapshot(migrated_engine: Engine) -> None:
    client = document_client(migrated_engine)

    response = client.post(
        "/documents",
        json=document_payload(body_text="Internal policy body v1"),
        headers=auth_headers(),
    )

    assert response.status_code == 201
    payload = response.json()
    assert payload["title"] == "AI Use Policy"
    assert payload["document_type"] == "company_policy"
    assert payload["body_text"] == "Internal policy body v1"
    assert payload["effective_date"] == "2026-05-19"
    assert payload["workspace_id"] == "ws-1"
    assert payload["snapshot_id"].startswith("snapshot_")

    with Session(migrated_engine) as session:
        stored = session.scalar(
            select(SourceDocument).where(
                SourceDocument.snapshot_id == payload["snapshot_id"]
            )
        )
    assert stored is not None
    assert stored.body_text == "Internal policy body v1"


def test_document_update_creates_new_snapshot(migrated_engine: Engine) -> None:
    client = document_client(migrated_engine)
    original = create_document(client, body_text="Internal policy body v1")

    update_response = client.put(
        f"/documents/{original['logical_document_id']}",
        json=document_payload(body_text="Internal policy body v2"),
        headers=auth_headers(),
    )

    assert update_response.status_code == 200
    updated = update_response.json()
    assert updated["snapshot_id"] != original["snapshot_id"]
    assert updated["version"] == 2

    previous_response = client.get(
        (
            f"/documents/{original['logical_document_id']}/snapshots/"
            f"{original['snapshot_id']}"
        ),
        headers=auth_headers(),
    )
    assert previous_response.status_code == 200
    assert previous_response.json()["body_text"] == "Internal policy body v1"


def test_document_body_not_logged(migrated_engine: Engine, caplog) -> None:
    client = document_client(migrated_engine)
    sensitive_body = "Sensitive SOP body should stay out of logs"

    with caplog.at_level(logging.INFO):
        original = create_document(client, body_text=sensitive_body)
        client.put(
            f"/documents/{original['logical_document_id']}",
            json=document_payload(body_text=f"{sensitive_body} updated"),
            headers=auth_headers(),
        )

    rendered_logs = "\n".join(record.getMessage() for record in caplog.records)
    assert sensitive_body not in rendered_logs
    assert f"{sensitive_body} updated" not in rendered_logs


def document_client(engine: Engine) -> TestClient:
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)
    app = create_app(
        settings=get_settings({"APP_ENV": "test"}), session_factory=session_factory
    )
    return TestClient(app)


def create_document(client: TestClient, *, body_text: str) -> dict:
    response = client.post(
        "/documents",
        json=document_payload(body_text=body_text),
        headers=auth_headers(),
    )
    assert response.status_code == 201
    return response.json()


def document_payload(*, body_text: str) -> dict[str, str]:
    return {
        "title": "AI Use Policy",
        "document_type": "company_policy",
        "body_text": body_text,
        "effective_date": "2026-05-19",
    }


def auth_headers() -> dict[str, str]:
    token = create_token(
        actor_id="operator-1",
        role="operator",
        workspace_id="ws-1",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-documents"}
