import subprocess
import sys


def test_pytest_collects_initial_suite() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "--collect-only", "tests", "-q"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    collected_tests = [line for line in result.stdout.splitlines() if "::test_" in line]
    assert len(collected_tests) >= 3


def test_ruff_check_command_succeeds() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "ruff", "check", "ai_rollout_os", "tests"],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stdout + result.stderr
