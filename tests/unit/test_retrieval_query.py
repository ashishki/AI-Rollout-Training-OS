import ast
import inspect
from pathlib import Path

from ai_rollout_os.retrieval.vector_repository import RetrievalQueryRepository


def test_query_uses_vector_fts_and_rrf() -> None:
    source = inspect.getsource(RetrievalQueryRepository.hybrid_search)

    assert "cosine_distance" in source
    assert "to_tsvector" in source
    assert "_reciprocal_rank_score" in source


def test_query_does_not_import_ingestion_module() -> None:
    module = ast.parse(Path("ai_rollout_os/retrieval/query.py").read_text())

    imported_modules = {
        alias.name
        for node in ast.walk(module)
        if isinstance(node, ast.Import)
        for alias in node.names
    }
    imported_from_modules = {
        node.module for node in ast.walk(module) if isinstance(node, ast.ImportFrom)
    }

    assert "ai_rollout_os.retrieval.ingestion" not in imported_modules
    assert "ai_rollout_os.retrieval.ingestion" not in imported_from_modules
    assert "ingestion" not in imported_modules
    assert "ingestion" not in imported_from_modules
