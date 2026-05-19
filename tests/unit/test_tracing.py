from pathlib import Path

from ai_rollout_os.observability.tracing import get_tracer


def test_shared_tracer_factory_is_used() -> None:
    tracer = get_tracer()

    assert tracer is get_tracer()
    with tracer.start_span("feedback.generate", {"email": "alice@example.com"}) as span:
        assert span.name == "feedback.generate"
        assert span.attributes["email"] == "[REDACTED]"

    for path in Path("ai_rollout_os").rglob("*.py"):
        if path.name == "tracing.py":
            continue
        assert "Tracer(" not in path.read_text()
