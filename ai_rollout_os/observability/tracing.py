from collections.abc import Iterator
from contextlib import contextmanager
from contextvars import ContextVar
from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4

from ai_rollout_os.observability.logging import redact_value

_trace_id: ContextVar[str | None] = ContextVar("trace_id", default=None)


def get_trace_id() -> str:
    existing = _trace_id.get()
    if existing:
        return existing
    new_trace_id = uuid4().hex
    _trace_id.set(new_trace_id)
    return new_trace_id


def set_trace_id(trace_id: str) -> None:
    _trace_id.set(trace_id)


@dataclass
class Span:
    name: str
    trace_id: str
    attributes: dict[str, Any] = field(default_factory=dict)

    def set_attribute(self, key: str, value: Any) -> None:
        self.attributes[key] = redact_value(key, value)


class Tracer:
    @contextmanager
    def start_span(
        self, name: str, attributes: dict[str, Any] | None = None
    ) -> Iterator[Span]:
        span = Span(name=name, trace_id=get_trace_id())
        for key, value in (attributes or {}).items():
            span.set_attribute(key, value)
        yield span


_TRACER = Tracer()


def get_tracer() -> Tracer:
    return _TRACER
