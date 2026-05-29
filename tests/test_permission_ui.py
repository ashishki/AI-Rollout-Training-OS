from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient


def test_permission_scenario_card_renders() -> None:
    client = TestClient(create_app(settings=get_settings({"APP_ENV": "test"})))

    response = client.get("/app/permission-simulator", headers=auth_headers())

    assert response.status_code == 200
    assert response.headers["content-type"].startswith("text/html")
    assert 'data-permission-simulator="true"' in response.text
    assert 'data-scenario-card="secrets-env-read"' in response.text
    assert 'data-scenario-request="true"' in response.text
    assert 'data-scenario-context="true"' in response.text
    assert 'data-decision-action="approve"' in response.text
    assert 'data-decision-action="deny"' in response.text
    assert "I need to read .env" in response.text


def test_permission_decision_result_renders() -> None:
    client = TestClient(create_app(settings=get_settings({"APP_ENV": "test"})))

    response = client.post(
        "/app/permission-simulator/decisions",
        headers=auth_headers(),
        data={"scenario_id": "secrets-env-read", "decision": "deny"},
    )

    assert response.status_code == 200
    assert 'data-permission-result="true"' in response.text
    assert 'data-score-outcome="correct"' in response.text
    assert 'data-consequence="true"' in response.text
    assert 'data-safer-path="true"' in response.text
    assert 'data-score-summary="true"' in response.text
    assert "Secret files are blocked input" in response.text
    assert "Ask the agent to inspect .env.example" in response.text


def test_public_permission_demo_renders_without_authentication() -> None:
    client = TestClient(create_app(settings=get_settings({"APP_ENV": "test"})))

    response = client.get("/demo/permission-simulator")

    assert response.status_code == 200
    assert 'data-role="demo"' in response.text
    assert 'data-permission-simulator="true"' in response.text
    assert 'action="/demo/permission-simulator/decisions"' in response.text
    assert "Agent Permission Simulator" in response.text


def test_public_permission_demo_decision_result_renders() -> None:
    client = TestClient(create_app(settings=get_settings({"APP_ENV": "test"})))

    response = client.post(
        "/demo/permission-simulator/decisions",
        data={"scenario_id": "secrets-env-read", "decision": "deny"},
    )

    assert response.status_code == 200
    assert 'data-role="demo"' in response.text
    assert 'data-score-outcome="correct"' in response.text
    assert "Secret files are blocked input" in response.text


def auth_headers() -> dict[str, str]:
    token = create_token(
        actor_id="permission-ui-learner",
        role="learner",
        workspace_id="ws-permission-ui",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-permission-ui"}
