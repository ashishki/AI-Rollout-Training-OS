from pathlib import Path

SCREENSHOT_PATH = Path("docs/audit/artifacts/permission_simulator_demo.png")
CAPTURE_SCRIPT_PATH = Path("scripts/capture_permission_simulator_demo.py")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def test_permission_simulator_browser_artifact_exists() -> None:
    assert SCREENSHOT_PATH.exists()
    assert SCREENSHOT_PATH.read_bytes().startswith(PNG_SIGNATURE)
    assert SCREENSHOT_PATH.stat().st_size > 10_000


def test_permission_simulator_browser_capture_is_reproducible() -> None:
    script = CAPTURE_SCRIPT_PATH.read_text()

    assert "/demo/permission-simulator" in script
    assert "--headless=new" in script
    assert "PERMISSION_SIMULATOR_SCREENSHOT" in script
    assert "google-chrome" in script
