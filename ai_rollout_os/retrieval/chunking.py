import re
from dataclasses import dataclass

import tiktoken
from ai_rollout_os.retrieval.constants import CHUNK_MAX_TOKENS, CHUNK_OVERLAP_TOKENS

_HEADING_RE = re.compile(r"^(?P<marks>#{1,6})\s+(?P<title>.+?)\s*$")
_ENCODING = tiktoken.get_encoding("cl100k_base")


@dataclass(frozen=True)
class TextChunk:
    section_path: str
    text: str
    chunk_index: int
    token_count: int
    start_token: int
    end_token: int


@dataclass(frozen=True)
class TextSection:
    section_path: str
    text: str


def token_count(text: str) -> int:
    return len(_ENCODING.encode(text))


def chunk_source_text(
    body_text: str,
    *,
    max_tokens: int = CHUNK_MAX_TOKENS,
    overlap_tokens: int = CHUNK_OVERLAP_TOKENS,
) -> list[TextChunk]:
    chunks: list[TextChunk] = []
    for section in _sections_from_markdown(body_text):
        section_tokens = _ENCODING.encode(section.text)
        if not section_tokens:
            continue

        step = max_tokens - overlap_tokens
        start = 0
        while start < len(section_tokens):
            end = min(start + max_tokens, len(section_tokens))
            chunk_tokens = section_tokens[start:end]
            chunks.append(
                TextChunk(
                    section_path=section.section_path,
                    text=_ENCODING.decode(chunk_tokens).strip(),
                    chunk_index=len(chunks),
                    token_count=len(chunk_tokens),
                    start_token=start,
                    end_token=end,
                )
            )
            if end == len(section_tokens):
                break
            start += step
    return chunks


def _sections_from_markdown(body_text: str) -> list[TextSection]:
    sections: list[TextSection] = []
    heading_stack: list[str] = []
    current_lines: list[str] = []

    def flush() -> None:
        text = "\n".join(current_lines).strip()
        if text:
            sections.append(
                TextSection(section_path=_section_path(heading_stack), text=text)
            )
        current_lines.clear()

    for raw_line in body_text.replace("\r\n", "\n").split("\n"):
        heading = _HEADING_RE.match(raw_line)
        if heading is None:
            current_lines.append(raw_line)
            continue

        flush()
        level = len(heading.group("marks"))
        title = heading.group("title").strip()
        heading_stack = heading_stack[: level - 1]
        heading_stack.append(title)

    flush()
    return sections or [TextSection(section_path="Document", text=body_text.strip())]


def _section_path(heading_stack: list[str]) -> str:
    if not heading_stack:
        return "Document"
    return " > ".join(heading_stack)
