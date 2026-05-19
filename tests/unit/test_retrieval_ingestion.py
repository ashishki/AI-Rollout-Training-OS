import ast
from pathlib import Path

from ai_rollout_os.retrieval.chunking import (
    CHUNK_MAX_TOKENS,
    CHUNK_OVERLAP_TOKENS,
    chunk_source_text,
    token_count,
)


def test_ingestion_does_not_import_query_module() -> None:
    module = ast.parse(Path("ai_rollout_os/retrieval/ingestion.py").read_text())

    imported_modules = {
        alias.name
        for node in ast.walk(module)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from_modules = {
        node.module for node in ast.walk(module) if isinstance(node, ast.ImportFrom)
    }

    assert "ai_rollout_os.retrieval.query" not in imported_modules
    assert "ai_rollout_os.retrieval.query" not in imported_from_modules
    assert "query" not in imported_modules
    assert "query" not in imported_from_modules


def test_chunks_respect_token_boundary_and_overlap() -> None:
    body_text = " ".join(f"token-{index}" for index in range(900))

    chunks = chunk_source_text(body_text)

    assert len(chunks) > 1
    assert all(chunk.token_count <= CHUNK_MAX_TOKENS for chunk in chunks)
    assert chunks[1].start_token == chunks[0].end_token - CHUNK_OVERLAP_TOKENS
    assert token_count(chunks[0].text) <= CHUNK_MAX_TOKENS


def test_chunking_preserves_markdown_section_paths() -> None:
    body_text = """# Policy

Intro text.

## Customer Data

Do not paste customer data into AI tools.

### Approval

Manager approval is required for workflow reuse.
"""

    chunks = chunk_source_text(body_text)

    section_paths = {chunk.section_path for chunk in chunks}
    assert "Policy > Customer Data" in section_paths
    assert "Policy > Customer Data > Approval" in section_paths
