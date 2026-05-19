from dataclasses import dataclass


@dataclass(frozen=True)
class EvidenceBlock:
    source_id: str
    section_path: str
    chunk_id: str
    score: float
    snippet: str


@dataclass(frozen=True)
class RetrievalResult:
    status: str
    evidence: list[EvidenceBlock]
    generated_answer: str | None = None
    reason: str | None = None


def citation_snippet(text: str, *, max_chars: int = 280) -> str:
    compact = " ".join(text.split())
    if len(compact) <= max_chars:
        return compact
    return f"{compact[: max_chars - 3].rstrip()}..."
