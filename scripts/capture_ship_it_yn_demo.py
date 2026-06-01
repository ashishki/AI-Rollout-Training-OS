from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

DEFAULT_URL = "http://127.0.0.1:8000/demo/ship-it-yn"
DEFAULT_DESKTOP_OUTPUT = "docs/audit/artifacts/ship_it_yn_desktop.png"
DEFAULT_MOBILE_OUTPUT = "docs/audit/artifacts/ship_it_yn_mobile.png"
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
VIEWPORTS = {
    "desktop": ("1440,1000", "SHIP_IT_YN_DESKTOP_SCREENSHOT", DEFAULT_DESKTOP_OUTPUT),
    "mobile": ("390,844", "SHIP_IT_YN_MOBILE_SCREENSHOT", DEFAULT_MOBILE_OUTPUT),
}


def main() -> int:
    url = os.environ.get("SHIP_IT_YN_DEMO_URL", DEFAULT_URL)
    browser = _find_browser()
    if browser is None:
        print(
            "No Chrome/Chromium browser found. Set BROWSER_BIN to a headless browser.",
            file=sys.stderr,
        )
        return 1

    for label, (window_size, env_name, default_output) in VIEWPORTS.items():
        output = Path(os.environ.get(env_name, default_output))
        output.parent.mkdir(parents=True, exist_ok=True)
        result = _capture(browser, url, window_size, output)
        if result != 0:
            return result
        if not _is_png(output):
            print(
                f"{label} screenshot was not written as a PNG: {output}",
                file=sys.stderr,
            )
            return 1
        print(f"Wrote {label} browser screenshot: {output}")
    return 0


def _capture(browser: str, url: str, window_size: str, output: Path) -> int:
    with tempfile.TemporaryDirectory(prefix="ship-it-yn-browser-") as profile:
        completed = subprocess.run(
            [
                browser,
                "--headless=new",
                "--no-sandbox",
                "--disable-dev-shm-usage",
                "--hide-scrollbars",
                f"--window-size={window_size}",
                f"--user-data-dir={profile}",
                f"--screenshot={output}",
                url,
            ],
            check=False,
        )
    return completed.returncode


def _is_png(path: Path) -> bool:
    return path.exists() and path.read_bytes()[: len(PNG_SIGNATURE)] == PNG_SIGNATURE


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
