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
        "src/components/DecisionButtons.tsx",
        "src/components/DecisionButtons.test.tsx",
        "src/components/DiffPreview.tsx",
        "src/components/DiffPreview.test.tsx",
        "src/components/AuditTrail.tsx",
        "src/components/AuditTrail.test.tsx",
        "src/components/BadgeToast.tsx",
        "src/components/BadgeToast.test.tsx",
        "src/components/ConsequencePanel.tsx",
        "src/components/ConsequencePanel.test.tsx",
        "src/components/RiskMeters.tsx",
        "src/components/RiskMeters.test.tsx",
        "src/components/ResultScreen.tsx",
        "src/components/ResultScreen.test.tsx",
        "src/components/ScenarioCard.tsx",
        "src/components/ScenarioCard.test.tsx",
        "src/components/TerminalLayout.tsx",
        "src/components/TerminalLayout.test.tsx",
        "src/components/TerminalLog.tsx",
        "src/styles.css",
        "src/game/scenarioTypes.ts",
        "src/game/shareText.ts",
        "src/game/shareText.test.ts",
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
    assert scenarios[0]["agentMessage"]
    assert scenarios[0]["toolCall"]["scope"] == "unscoped_cleanup"
    assert scenarios[0]["context"][0]["label"] == "proposed cleanup"
    assert scenarios[0]["inspectArtifacts"][0]["id"] == (
        "artifact-tiny-cleanup-preview"
    )
    assert scenarios[0]["feedback"]["restrict_scope"]["outcome"] == "correct"
    assert scenarios[0]["feedback"]["restrict_scope"]["scoreDelta"] == 15
    assert scenarios[0]["badges"] == ["scope_before_delete"]
    assert "restrict_scope" in scenarios[0]["choices"]


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
