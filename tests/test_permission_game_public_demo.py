from pathlib import Path

import frontend.app_shell as app_shell
from ai_rollout_os.core.config import get_settings
from ai_rollout_os.main import create_app
from fastapi.testclient import TestClient


def test_public_ship_it_yn_route_renders(tmp_path, monkeypatch) -> None:
    dist = _write_demo_build(tmp_path)
    monkeypatch.setattr(app_shell, "SHIP_IT_YN_DIST_DIR", dist)
    client = TestClient(create_app(settings=get_settings({"APP_ENV": "test"})))

    response = client.get("/demo/ship-it-yn")

    assert response.status_code == 200
    assert '<div id="root"></div>' in response.text
    assert "/demo/ship-it-yn/assets/index.js" in response.text

    asset_response = client.get("/demo/ship-it-yn/assets/index.js")
    assert asset_response.status_code == 200
    assert "console.log" in asset_response.text


def test_public_ship_it_yn_route_handles_missing_build(tmp_path, monkeypatch) -> None:
    monkeypatch.setattr(app_shell, "SHIP_IT_YN_DIST_DIR", tmp_path / "missing-dist")
    client = TestClient(create_app(settings=get_settings({"APP_ENV": "test"})))

    response = client.get("/demo/ship-it-yn")

    assert response.status_code == 200
    assert 'data-ship-it-yn-missing-build="true"' in response.text
    assert "npm run build" in response.text
    assert "<script" not in response.text


def _write_demo_build(tmp_path: Path) -> Path:
    dist = tmp_path / "dist"
    assets = dist / "assets"
    assets.mkdir(parents=True)
    (dist / "index.html").write_text(
        '<div id="root"></div><script type="module" src="/assets/index.js"></script>',
        encoding="utf-8",
    )
    (assets / "index.js").write_text("console.log('ship-it-yn');", encoding="utf-8")
    return dist
