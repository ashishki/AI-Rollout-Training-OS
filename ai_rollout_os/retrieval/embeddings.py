import hashlib
from collections.abc import Sequence
from typing import Protocol

from ai_rollout_os.retrieval.constants import VECTOR_DIMENSIONS


class EmbeddingClient(Protocol):
    model: str
    dimensions: int

    def embed_texts(self, texts: list[str]) -> list[list[float]]: ...


class HashEmbeddingClient:
    """Deterministic CI-safe embedding adapter for ingestion tests and bootstrap."""

    model = "test-hash-embedding"
    dimensions = VECTOR_DIMENSIONS

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        return [_hash_embedding(text, self.dimensions) for text in texts]


def validate_embeddings(
    embeddings: Sequence[Sequence[float]], *, expected_count: int, dimensions: int
) -> None:
    if len(embeddings) != expected_count:
        raise ValueError("Embedding count does not match chunk count")
    if any(len(embedding) != dimensions for embedding in embeddings):
        raise ValueError("Embedding dimensions do not match index schema")


def _hash_embedding(text: str, dimensions: int) -> list[float]:
    digest = hashlib.sha256(text.encode("utf-8")).digest()
    return [float(digest[index] / 255.0) for index in range(dimensions)]
