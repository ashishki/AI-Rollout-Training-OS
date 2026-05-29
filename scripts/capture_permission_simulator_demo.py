from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_URL = "http://127.0.0.1:8000/demo/permission-simulator"
DEFAULT_OUTPUT = "docs/audit/artifacts/permission_simulator_demo.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def main() -> int:
    url = os.environ.get("PERMISSION_SIMULATOR_DEMO_URL", DEFAULT_URL)
    output = Path(os.environ.get("PERMISSION_SIMULATOR_SCREENSHOT", DEFAULT_OUTPUT))
    browser = _find_browser()
    if browser is None:
        print(
            "No Chrome/Chromium browser found. Set BROWSER_BIN to a headless browser.",
            file=sys.stderr,
        )
        return 1

    output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="permission-simulator-browser-") as profile:
        command = [
            browser,
            "--headless=new",
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--hide-scrollbars",
            "--window-size=1440,1000",
            f"--user-data-dir={profile}",
            f"--screenshot={output}",
            url,
        ]
        completed = subprocess.run(command, check=False)

    if completed.returncode != 0:
        return completed.returncode

    if (
        not output.exists()
        or output.read_bytes()[: len(PNG_SIGNATURE)] != PNG_SIGNATURE
    ):
        print(f"Screenshot was not written as a PNG: {output}", file=sys.stderr)
        return 1

    print(f"Wrote browser screenshot: {output}")
    return 0


def _find_browser() -> str | None:
    configured = os.environ.get("BROWSER_BIN")
    if configured:
        return configured
    for candidate in ("google-chrome", "chromium", "chromium-browser"):
        browser = shutil.which(candidate)
        if browser:
            return browser
    return None


if __name__ == "__main__":
    raise SystemExit(main())
