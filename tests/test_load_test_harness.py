import json
from pathlib import Path

import scripts.load_test as load_test


def test_load_test_script_exists_and_reports_required_metrics(tmp_path: Path) -> None:
    output = tmp_path / "load-test.json"

    exit_code = load_test.main(["--iterations", "12", "--output", str(output)])

    assert exit_code == 0
    report = json.loads(output.read_text())
    assert report["source"] == "synthetic-load-test-v1"
    assert report["iterations_per_scenario"] == 12

    scenarios = {summary["scenario"]: summary for summary in report["scenarios"]}
    assert set(scenarios) == {
        "cohort_launch",
        "retrieval_query",
        "feedback_job",
        "reminder_scheduler",
        "report_generation",
    }
    for summary in scenarios.values():
        assert summary["sample_count"] == 12
        assert summary["p95_latency_ms"] >= summary["median_latency_ms"]
        assert summary["p99_latency_ms"] >= summary["p95_latency_ms"]
        assert summary["max_latency_ms"] >= summary["p99_latency_ms"]


def test_load_test_rejects_zero_iterations() -> None:
    try:
        load_test.run_load_test(iterations=0)
    except ValueError as exc:
        assert str(exc) == "iterations must be at least 1"
    else:
        raise AssertionError("Expected load test iteration validation to fail")
