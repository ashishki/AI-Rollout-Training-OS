import os
import shutil
import socket
import subprocess
import sys
import time
from urllib.request import urlopen


def test_ship_it_yn_keyboard_path() -> None:
    _ensure_frontend_build()
    port = _free_port()
    server = _start_server(port)
    try:
        _wait_for_url(f"http://127.0.0.1:{port}/health")
        completed = subprocess.run(
            [
                _browser_bin(),
                "--headless=new",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--dump-dom",
                f"http://127.0.0.1:{port}/demo/ship-it-yn",
            ],
            check=False,
            capture_output=True,
            text=True,
        )

        assert completed.returncode == 0
        dom = completed.stdout
        assert 'aria-label="Выбор роли"' in dom
        assert ">Менеджер<" in dom
        assert ">Тимлид / фасилитатор<" in dom
        assert ">Разработчик<" in dom
        assert "Тренажёр разрешений" in dom
    finally:
        server.terminate()
        server.wait(timeout=10)


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
    raise AssertionError("No Chrome/Chromium browser found for accessibility test")


def _start_server(port: int) -> subprocess.Popen:
    env = {**os.environ, "APP_ENV": "test"}
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
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
