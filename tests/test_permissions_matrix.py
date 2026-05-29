from pathlib import Path

from ai_rollout_os.auth.permissions import PERMISSIONS, ROUTE_PERMISSIONS
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.main import create_app
from fastapi.routing import APIRoute

PROTECTED_METHODS = {"DELETE", "GET", "PATCH", "POST", "PUT"}


def test_every_route_has_permission() -> None:
    app = create_app(settings=get_settings({"APP_ENV": "test"}))
    route_permissions = {}
    for route in app.routes:
        if not isinstance(route, APIRoute) or route.path == "/health":
            continue
        if getattr(route.endpoint, "public_design_decision", None):
            continue
        for method in sorted(route.methods & PROTECTED_METHODS):
            permission_names = [
                permission_name
                for dependency in route.dependant.dependencies
                if (
                    permission_name := getattr(dependency.call, "permission_name", None)
                )
            ]
            route_permissions[(method, route.path)] = permission_names

    assert set(route_permissions) == set(ROUTE_PERMISSIONS)
    for route_key, expected_permission in ROUTE_PERMISSIONS.items():
        assert expected_permission in PERMISSIONS
        assert route_permissions[route_key] == [expected_permission]


def test_public_routes_cite_design_decision() -> None:
    app = create_app(settings=get_settings({"APP_ENV": "test"}))
    public_routes = {
        route.path: getattr(route.endpoint, "public_design_decision", None)
        for route in app.routes
        if isinstance(route, APIRoute)
        and getattr(route.endpoint, "public_design_decision", None)
    }

    assert public_routes == {
        "/demo/permission-simulator": "D-012 static public permission simulator demo",
        "/demo/permission-simulator/decisions": (
            "D-012 static public permission simulator demo"
        ),
    }


def test_permission_matrix_roles_are_documented() -> None:
    text = "\n".join(
        f"`{permission.name}` | {', '.join(sorted(permission.allowed_roles))}"
        for permission in PERMISSIONS.values()
    )
    security_review = Path("docs/security_review.md").read_text()

    for line in text.splitlines():
        assert line in security_review
