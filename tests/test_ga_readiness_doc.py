from pathlib import Path


def test_ga_readiness_doc_complete() -> None:
    readiness = Path("docs/ga_readiness.md").read_text()

    assert "# GA Readiness Checklist" in readiness
    assert "Status: NOT READY FOR GA" in readiness
    assert "## Product Gate" in readiness
    assert "## Security Gate" in readiness
    assert "## Reliability Gate" in readiness
    assert "## AI Quality Gate" in readiness
    assert "## Support Gate" in readiness
    assert "## GTM Gate" in readiness
    assert "## GA Exit Decision" in readiness
    assert "no open P0/P1 findings" in readiness
    assert "browser automation" in readiness
    assert "paid customer or signed expansion path" in readiness
    assert "Customer admin documentation" in readiness
