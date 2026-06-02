import os
import shutil
import socket
import subprocess
import time
from pathlib import Path
from urllib.request import urlopen

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
APP_URL_PATH = "/demo/ship-it-yn"


def test_ship_it_yn_responsive_screenshots(tmp_path: Path) -> None:
    browser = _browser_bin()
    _ensure_frontend_build()
    port = _free_port()
    server = _start_server(port)
    try:
        _wait_for_url(f"http://127.0.0.1:{port}/health")
        screenshots = {
            "desktop": ("1440,1000", tmp_path / "ship_it_yn_desktop.png"),
            "tablet": ("900,1100", tmp_path / "ship_it_yn_tablet.png"),
            "mobile": ("390,844", tmp_path / "ship_it_yn_mobile.png"),
        }
        for viewport, output in screenshots.values():
            completed = subprocess.run(
                [
                    browser,
                    "--headless=new",
                    "--no-sandbox",
                    "--disable-dev-shm-usage",
                    "--hide-scrollbars",
                    f"--window-size={viewport}",
                    f"--screenshot={output}",
                    f"http://127.0.0.1:{port}{APP_URL_PATH}",
                ],
                check=False,
            )
            assert completed.returncode == 0
            assert output.read_bytes().startswith(PNG_SIGNATURE)
            assert output.stat().st_size > 10_000
    finally:
        server.terminate()
        server.wait(timeout=10)


def test_ship_it_yn_controls_do_not_shift_layout() -> None:
    styles = Path("frontend/permission_game/src/styles.css").read_text()

    assert ".terminal-action-button {" in styles
    assert "min-height: 3rem;" in styles
    assert ".terminal-action-button:hover {" in styles
    assert ".terminal-action-button:focus-visible {" in styles
    assert '.terminal-action-button[aria-disabled="true"]' in styles
    assert "outline-offset: 2px;" in styles
    assert "align-items: stretch;" in styles
    assert ".mission-track {" in styles
    assert ".agent-pulse {" in styles
    assert ".role-card-visual {" in styles


def _ensure_frontend_build() -> None:
    completed = subprocess.run(
        ["npm", "run", "build"],
        cwd="frontend/permission_game",
        check=False,
    )
    assert completed.returncode == 0


def _browser_bin() -> str:
    configured = os.environ.get("BROWSER_BIN")
    if configured:
        return configured
    for candidate in ("google-chrome", "chromium", "chromium-browser"):
        browser = shutil.which(candidate)
        if browser:
            return browser
    raise AssertionError("No Chrome/Chromium browser found for visual test")


def _start_server(port: int) -> subprocess.Popen:
    env = {**os.environ, "APP_ENV": "test"}
    return subprocess.Popen(
        [
            ".venv/bin/uvicorn",
            "ai_rollout_os.main:app",
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _wait_for_url(url: str) -> None:
    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            with urlopen(url, timeout=1) as response:
                if response.status == 200:
                    return
        except OSError:
            time.sleep(0.2)
    raise AssertionError(f"Server did not become ready: {url}")


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])
