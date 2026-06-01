import base64
import json
import os
import shutil
import socket
import struct
import subprocess
import tempfile
import time
from urllib.parse import urlparse
from urllib.request import urlopen


def test_public_ship_it_yn_full_run() -> None:
    _ensure_frontend_build()
    app_port = _free_port()
    debug_port = _free_port()
    server = _start_server(app_port)
    browser = _start_browser(app_port, debug_port)
    try:
        _wait_for_url(f"http://127.0.0.1:{app_port}/health")
        client = _DevToolsClient.from_debug_port(
            debug_port, f"http://127.0.0.1:{app_port}/demo/ship-it-yn"
        )
        _wait_for_text(client, "Tiny Cleanup")

        _click_text(client, "Inspect")
        _click_text(client, "Restrict Scope")
        _click_text(client, "Next Level")
        _click_text(client, "Require Eval")
        _click_text(client, "Next Level")
        _click_text(client, "Deny")
        _click_text(client, "Next Level")
        _click_text(client, "Escalate")
        _click_text(client, "Next Level")
        _click_text(client, "Sandbox")
        _click_text(client, "Next Level")
        _click_text(client, "Require Eval")
        _click_text(client, "Next Level")
        _click_text(client, "Sandbox")
        _click_text(client, "Show Final Report")

        body_text = (
            client.evaluate("document.body.innerText")
            .get("result", {})
            .get("value", "")
        )
        share_text = client.evaluate(
            "document.querySelector('textarea[aria-label=\"Share text\"]').value"
        )["result"]["value"]
        assert "Seven-level public demo complete" in body_text
        assert "FINAL REPORT" in body_text
        assert "84/100" in body_text
        assert "Copy Share" in body_text
        assert "Ship It? Y/N score:" in share_text
    finally:
        browser.terminate()
        server.terminate()
        browser.wait(timeout=10)
        server.wait(timeout=10)


def test_public_ship_it_yn_has_no_external_execution() -> None:
    _ensure_frontend_build()
    app_port = _free_port()
    debug_port = _free_port()
    server = _start_server(app_port)
    browser = _start_browser(app_port, debug_port)
    try:
        _wait_for_url(f"http://127.0.0.1:{app_port}/health")
        client = _DevToolsClient.from_debug_port(
            debug_port, f"http://127.0.0.1:{app_port}/demo/ship-it-yn"
        )
        _wait_for_text(client, "Tiny Cleanup")
        resources = client.evaluate(
            "performance.getEntriesByType('resource').map((entry) => entry.name)"
        )["result"]["value"]
        body_text = client.evaluate("document.body.innerText")["result"]["value"]

        assert resources
        assert all(
            resource.startswith(f"http://127.0.0.1:{app_port}/")
            for resource in resources
        ), resources
        assert "Bearer " not in body_text
        assert "file://" not in body_text
        assert "localhost:" not in body_text
    finally:
        browser.terminate()
        server.terminate()
        browser.wait(timeout=10)
        server.wait(timeout=10)


def test_public_ship_it_yn_has_no_tracking_network_calls() -> None:
    _ensure_frontend_build()
    app_port = _free_port()
    debug_port = _free_port()
    server = _start_server(app_port)
    browser = _start_browser(app_port, debug_port)
    try:
        _wait_for_url(f"http://127.0.0.1:{app_port}/health")
        client = _DevToolsClient.from_debug_port(
            debug_port, f"http://127.0.0.1:{app_port}/demo/ship-it-yn"
        )
        _wait_for_text(client, "Tiny Cleanup")
        resources = client.evaluate(
            "performance.getEntriesByType('resource').map((entry) => entry.name)"
        )["result"]["value"]
        analytics_snapshot = client.evaluate(
            "localStorage.getItem('ship-it-yn-analytics-v1')"
        )["result"]["value"]

        forbidden_fragments = [
            "/analytics",
            "/track",
            "/collect",
            "segment",
            "amplitude",
            "posthog",
            "google-analytics",
        ]
        assert all(
            fragment not in resource
            for resource in resources
            for fragment in forbidden_fragments
        )
        assert analytics_snapshot
        assert "sessionsStarted" in analytics_snapshot
        for forbidden in ["actor_id", "workspace_id", "learner", "email", "customer"]:
            assert forbidden not in analytics_snapshot
    finally:
        browser.terminate()
        server.terminate()
        browser.wait(timeout=10)
        server.wait(timeout=10)


def _click_text(client: "_DevToolsClient", label: str) -> None:
    expression = f"""
    (() => {{
      const target = [...document.querySelectorAll('button')]
        .find((button) => button.textContent.trim().includes({json.dumps(label)}));
      if (!target) return false;
      target.click();
      return true;
    }})()
    """
    assert client.evaluate(expression)["result"]["value"] is True
    time.sleep(0.15)


def _wait_for_text(client: "_DevToolsClient", text: str) -> None:
    deadline = time.time() + 15
    expression = f"document.body.innerText.includes({json.dumps(text)})"
    while time.time() < deadline:
        if client.evaluate(expression)["result"].get("value") is True:
            return
        time.sleep(0.2)
    raise AssertionError(f"Browser page did not render expected text: {text}")


def _ensure_frontend_build() -> None:
    completed = subprocess.run(
        ["npm", "run", "build"],
        cwd="frontend/permission_game",
        check=False,
    )
    assert completed.returncode == 0


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


def _start_browser(app_port: int, debug_port: int) -> subprocess.Popen:
    profile = tempfile.TemporaryDirectory(prefix="ship-it-yn-cdp-")
    process = subprocess.Popen(
        [
            _browser_bin(),
            "--headless=new",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--remote-allow-origins=*",
            f"--remote-debugging-port={debug_port}",
            f"--user-data-dir={profile.name}",
            f"http://127.0.0.1:{app_port}/demo/ship-it-yn",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    process._profile_dir = profile  # type: ignore[attr-defined]
    return process


def _browser_bin() -> str:
    configured = os.environ.get("BROWSER_BIN")
    if configured:
        return configured
    for candidate in ("google-chrome", "chromium", "chromium-browser"):
        browser = shutil.which(candidate)
        if browser:
            return browser
    raise AssertionError("No Chrome/Chromium browser found for gameplay test")


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


class _DevToolsClient:
    def __init__(self, sock: socket.socket) -> None:
        self.sock = sock
        self.next_id = 1

    @classmethod
    def from_debug_port(cls, debug_port: int, target_url: str) -> "_DevToolsClient":
        deadline = time.time() + 15
        websocket_url = ""
        while time.time() < deadline:
            try:
                with urlopen(f"http://127.0.0.1:{debug_port}/json", timeout=1) as res:
                    pages = json.loads(res.read().decode())
                for page in pages:
                    if page.get("type") == "page" and page.get("url") == target_url:
                        websocket_url = page["webSocketDebuggerUrl"]
                        break
                if websocket_url:
                    break
            except OSError:
                time.sleep(0.2)
            time.sleep(0.2)
        if not websocket_url:
            raise AssertionError("Chrome DevTools endpoint did not become ready")

        parsed = urlparse(websocket_url)
        sock = socket.create_connection((parsed.hostname, parsed.port), timeout=5)
        key = base64.b64encode(os.urandom(16)).decode()
        request = (
            f"GET {parsed.path} HTTP/1.1\r\n"
            f"Host: {parsed.hostname}:{parsed.port}\r\n"
            "Upgrade: websocket\r\n"
            "Connection: Upgrade\r\n"
            f"Origin: http://{parsed.hostname}:{parsed.port}\r\n"
            f"Sec-WebSocket-Key: {key}\r\n"
            "Sec-WebSocket-Version: 13\r\n\r\n"
        )
        sock.sendall(request.encode())
        response = sock.recv(4096)
        if not response.startswith(b"HTTP/1.1 101") or b"Upgrade:" not in response:
            raise AssertionError(
                f"Chrome DevTools websocket upgrade failed: {response!r}"
            )
        return cls(sock)

    def evaluate(self, expression: str) -> dict:
        command_id = self.next_id
        self.next_id += 1
        self._send(
            {
                "id": command_id,
                "method": "Runtime.evaluate",
                "params": {
                    "expression": expression,
                    "awaitPromise": True,
                    "returnByValue": True,
                },
            }
        )
        while True:
            message = self._recv()
            if message.get("id") == command_id:
                if "exceptionDetails" in message:
                    raise AssertionError(message["exceptionDetails"])
                return message["result"]

    def _send(self, payload: dict) -> None:
        data = json.dumps(payload).encode()
        header = bytearray([0x81])
        if len(data) < 126:
            header.append(0x80 | len(data))
        elif len(data) < 65536:
            header.append(0x80 | 126)
            header.extend(struct.pack("!H", len(data)))
        else:
            header.append(0x80 | 127)
            header.extend(struct.pack("!Q", len(data)))
        mask = os.urandom(4)
        header.extend(mask)
        masked = bytes(byte ^ mask[index % 4] for index, byte in enumerate(data))
        self.sock.sendall(header + masked)

    def _recv(self) -> dict:
        first = self.sock.recv(2)
        if len(first) < 2:
            raise AssertionError("Incomplete websocket frame")
        length = first[1] & 0x7F
        if length == 126:
            length = struct.unpack("!H", self._read_exact(2))[0]
        elif length == 127:
            length = struct.unpack("!Q", self._read_exact(8))[0]
        payload = self._read_exact(length)
        return json.loads(payload.decode())

    def _read_exact(self, length: int) -> bytes:
        chunks = bytearray()
        while len(chunks) < length:
            chunk = self.sock.recv(length - len(chunks))
            if not chunk:
                raise AssertionError("Websocket closed")
            chunks.extend(chunk)
        return bytes(chunks)
