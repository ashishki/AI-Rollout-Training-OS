from html.parser import HTMLParser

from ai_rollout_os.auth.tokens import create_token
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient


def test_role_navigation_shell() -> None:
    client = TestClient(create_app(settings=get_settings({"APP_ENV": "test"})))

    expectations = {
        "operator": ["Policies", "Role Packs", "Missions", "Guardrails", "Cohorts"],
        "manager": ["Review Queue", "Dashboard", "Reports", "Approvals"],
        "learner": ["Assignments", "Guardrail Quiz", "Submissions", "Feedback"],
    }
    for role, labels in expectations.items():
        response = client.get(
            "/app",
            headers=auth_headers(role),
        )
        parser = LinkTextParser()
        parser.feed(response.text)

        assert response.status_code == 200
        assert response.headers["content-type"].startswith("text/html")
        assert f'data-role="{role}"' in response.text
        assert f"{role.title()} Workspace" in response.text
        assert labels == parser.link_texts
        assert "landing" not in response.text.lower()


def test_protected_views_require_authentication() -> None:
    client = TestClient(create_app(settings=get_settings({"APP_ENV": "test"})))

    missing = client.get("/app")
    invalid = client.get("/app", headers={"authorization": "Bearer invalid"})
    unsupported_role = client.get("/app", headers=auth_headers("auditor"))

    assert missing.status_code == 401
    assert invalid.status_code == 401
    assert unsupported_role.status_code == 403


def auth_headers(role: str) -> dict[str, str]:
    token = create_token(
        actor_id=f"{role}-actor",
        role=role,
        workspace_id="ws-frontend",
        secret_key=get_settings({"APP_ENV": "test"}).secret_key,
    )
    return {"authorization": f"Bearer {token}", "x-trace-id": "trace-frontend"}


class LinkTextParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.link_texts: list[str] = []
        self._in_link = False

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        if tag == "a":
            self._in_link = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "a":
            self._in_link = False

    def handle_data(self, data: str) -> None:
        if self._in_link:
            self.link_texts.append(data.strip())
