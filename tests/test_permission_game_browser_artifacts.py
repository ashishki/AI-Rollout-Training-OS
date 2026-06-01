import struct
from pathlib import Path

DESKTOP_SCREENSHOT = Path("docs/audit/artifacts/ship_it_yn_desktop.png")
MOBILE_SCREENSHOT = Path("docs/audit/artifacts/ship_it_yn_mobile.png")
CAPTURE_SCRIPT = Path("scripts/capture_ship_it_yn_demo.py")
README = Path("README.md")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def test_ship_it_yn_browser_artifacts_exist() -> None:
    desktop_width, desktop_height = _png_dimensions(DESKTOP_SCREENSHOT)
    mobile_width, mobile_height = _png_dimensions(MOBILE_SCREENSHOT)
    script = CAPTURE_SCRIPT.read_text()

    assert DESKTOP_SCREENSHOT.stat().st_size > 10_000
    assert MOBILE_SCREENSHOT.stat().st_size > 10_000
    assert desktop_width >= 1200
    assert desktop_height >= 800
    assert 350 <= mobile_width <= 500
    assert mobile_height >= 700
    assert "/demo/ship-it-yn" in script
    assert "--headless=new" in script
    assert "SHIP_IT_YN_DEMO_URL" in script
    assert "SHIP_IT_YN_DESKTOP_SCREENSHOT" in script
    assert "SHIP_IT_YN_MOBILE_SCREENSHOT" in script


def test_readme_references_ship_it_yn_visual_artifact() -> None:
    readme = README.read_text()

    assert "/demo/ship-it-yn" in readme
    assert "docs/audit/artifacts/ship_it_yn_desktop.png" in readme
    assert "docs/audit/artifacts/ship_it_yn_mobile.png" in readme


def _png_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    assert data.startswith(PNG_SIGNATURE)
    return struct.unpack(">II", data[16:24])
