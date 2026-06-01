import json
from pathlib import Path

FRONTEND_DIR = Path("frontend/permission_game")


def test_permission_game_frontend_scaffold_exists() -> None:
    package = json.loads((FRONTEND_DIR / "package.json").read_text())

    assert package["scripts"] == {
        "dev": "vite --host 127.0.0.1",
        "build": "tsc -b && vite build",
        "lint": "eslint . --max-warnings=0",
        "test": "vitest run",
        "typecheck": "tsc -b",
    }

    for required in [
        "index.html",
        "vite.config.ts",
        "tsconfig.json",
        "tailwind.config.ts",
        "postcss.config.js",
        "src/main.tsx",
        "src/App.tsx",
        "src/App.test.tsx",
        "src/components/TerminalLayout.tsx",
        "src/components/TerminalLayout.test.tsx",
        "src/components/TerminalLog.tsx",
        "src/styles.css",
        "src/game/scenarioTypes.ts",
        "src/data/shipItYnScenarios.json",
    ]:
        assert (FRONTEND_DIR / required).exists()


def test_permission_game_imports_typed_scenario_data() -> None:
    app = (FRONTEND_DIR / "src/App.tsx").read_text()
    scenarios = json.loads(
        (FRONTEND_DIR / "src/data/shipItYnScenarios.json").read_text()
    )

    assert "PermissionGameScenarioSummary" in app
    assert "shipItYnScenarios.json" in app
    assert len(scenarios) == 7
    assert [scenario["level"] for scenario in scenarios] == list(range(1, 8))
    assert scenarios[0]["title"] == "Tiny Cleanup"


def test_permission_game_shell_blocks_lms_chrome() -> None:
    source_text = "\n".join(
        path.read_text()
        for path in sorted((FRONTEND_DIR / "src").glob("**/*"))
        if path.is_file() and path.suffix in {".ts", ".tsx", ".css"}
    ).lower()

    for forbidden in [
        "lms",
        "course",
        "cohort",
        "learner dashboard",
        "operator dashboard",
        "manager dashboard",
        "marketing hero",
    ]:
        assert forbidden not in source_text
