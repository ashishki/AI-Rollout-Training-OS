import tomllib
from pathlib import Path


def test_pyproject_declares_required_metadata() -> None:
    pyproject = tomllib.loads(Path("pyproject.toml").read_text())

    assert pyproject["project"]["name"] == "ai-rollout-training-os"
    assert pyproject["project"]["requires-python"] == ">=3.12"
    assert pyproject["tool"]["pytest"]["ini_options"]["testpaths"] == ["tests"]

    ruff_config = pyproject["tool"]["ruff"]
    assert ruff_config["target-version"] == "py312"
    assert "ai_rollout_os" in ruff_config["src"]
    assert "frontend" in ruff_config["src"]
    assert "tests" in ruff_config["src"]
