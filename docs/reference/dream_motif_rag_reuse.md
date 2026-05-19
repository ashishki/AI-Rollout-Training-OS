# Dream Motif Interpreter RAG Reuse Reference

Source repository: `https://github.com/ashishki/Dream_Motif_Interpreter`
Reviewed on: 2026-05-19

This file is a reuse map for AI Rollout Training OS. It is not canonical architecture by itself; `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, and `docs/tasks.md` remain authoritative.

---

## Reuse Decision

Use the Dream Motif Interpreter RAG implementation as the starting point for AI Rollout Training OS retrieval and retrieval evaluation.

The reusable core is:

- PostgreSQL 16 + pgvector as the vector store.
- Async SQLAlchemy session pattern and Alembic migration style.
- `EmbeddingClient` protocol and OpenAI embedding adapter shape.
- Paragraph/token chunking with `tiktoken`, 512-token max chunks, and overlap.
- Separate ingestion and query modules.
- Hybrid retrieval: pgvector cosine candidates plus PostgreSQL FTS candidates, fused with reciprocal rank fusion.
- `InsufficientEvidence` return type and no-answer behavior.
- Markdown-backed `docs/retrieval_eval.md` with evaluation dataset, baseline/current metrics, no-answer behavior, and evaluation history.
- `scripts/eval.py` pattern that seeds a synthetic corpus, computes hit@3, hit@5, MRR, citation precision, no-answer accuracy, and retrieval latency, and writes metrics back to the eval doc.
- Unit/integration test patterns for ingestion/query separation, chunk token boundaries, idempotent indexing, no-answer behavior, eval history validation, and CI-safe stub embeddings.

## Source Files To Study During Implementation

| Source path | Reuse value | Adaptation required |
|-------------|-------------|---------------------|
| `app/retrieval/types.py` | `SourceDocumentRef`, `FetchedSourceDocument`, `NormalizedDocument`, `SourceConnector`, `EmbeddingClient`, `OpenAIEmbeddingClient` | Rename domain-neutral types only where needed; remove dream-specific candidate types unless useful for policy document parsing. |
| `app/retrieval/ingestion.py` | `RagIngestionService`, chunking, embedding batching, vector literal conversion, normalized document helpers, idempotent upsert pattern | Replace `DreamEntry` / `DreamChunk` with policy/SOP document and chunk models; preserve schema versioning and separate ingestion/query boundary. |
| `app/retrieval/query.py` | `RagQueryService`, `EvidenceBlock`, `InsufficientEvidence`, FTS + vector RRF SQL, threshold handling, exact search pattern | Replace dream-specific columns and fragment matching with policy/SOP/source citation fields; remove dream-symbolic query expansion profiles. |
| `scripts/eval.py` | Eval dataset parser, metric calculation, stub embeddings, seeded DB setup, markdown update functions | Replace seed dreams with policy/SOP/role-pack fixture documents and expected source IDs. Keep Eval Source, Date, Corpus Version requirements. |
| `docs/retrieval_eval.md` | Mature retrieval eval artifact shape with regression datasets and history | Keep this project's own policy/SOP query set, but reuse table structures and metric lifecycle. |
| `tests/unit/test_rag_ingestion.py` | Chunk boundary, tiktoken, ingestion/query import separation, duplicate hash handling, embedding error tests | Adapt to policy document chunks and redaction constraints. |
| `tests/integration/test_rag_ingestion.py` | pgvector migration, idempotent indexing, embedding dimension checks | Adapt to document snapshots and workspace/policy snapshot fields. |
| `tests/unit/test_rag_query.py` | Query/ingestion separation, FTS coverage, embedding error handling, `InsufficientEvidence`, row merge/dedupe tests | Adapt to source citations and text-only policy corpus. |
| `tests/integration/test_rag_query.py` | Evidence blocks, no-match threshold, keyword-only hybrid search, stale index health degradation | Adapt to policy/SOP chunk tables and health readiness fields. |
| `tests/unit/test_retrieval_eval.py` | Eval dataset coverage and eval-history validity checks | Adapt expected sections and query IDs to AI Rollout Training OS. |
| `tests/integration/test_retrieval_eval.py` | End-to-end eval run with seeded database and no-answer assertions | Adapt fixture corpus and metrics thresholds. |
| `tests/unit/test_eval_script.py` | Markdown history append and no-write flag tests | Reuse with project-specific script/module names. |
| `alembic/versions/001_initial_schema.py` | `CREATE EXTENSION IF NOT EXISTS vector`, `Vector1536`, chunk table pattern | Adapt table names and metadata fields. |
| `alembic/versions/006_add_hnsw_index.py` | HNSW index migration for vector cosine ops | Adapt index/table/column names and keep concurrent index creation. |

## Must Preserve

- Ingestion and query-time retrieval stay in separate modules and tests enforce the import boundary.
- `insufficient_evidence` is a first-class result, not an exception and not a generated answer.
- Evaluation history rows include Date, Task, Corpus Version, Eval Source, and primary metrics.
- CI-safe eval can run with stub embeddings when provider keys are absent or test-prefixed.
- Vector schema version changes require ADR and re-index.
- Tests cover no-answer queries, exact/FTS fallback, idempotent indexing, and stale index health/readiness.

## Must Change

- Replace dream domain models with:
  - source documents / policy snapshots
  - document chunks
  - mission/rubric references
  - workspace ID
  - source citation metadata
- Replace dream-specific query expansion with policy/SOP query construction grounded in mission, rubric, learner answer, and policy question.
- Replace matched dream fragments with citation fields: source ID, section path, chunk ID, score, and snippet.
- Replace synthetic dream fixture with a synthetic policy/SOP/role-pack corpus that matches `docs/retrieval_eval.md`.
- Keep sensitive policy, SOP, and learner text out of logs, spans, metrics labels, and eval output beyond controlled snippets.

## Non-Reuse

Do not copy these domain-specific behaviors into AI Rollout Training OS:

- Dream symbolic query profiles.
- Russian religious/fish query regression logic.
- `DreamEntry`, `DreamTheme`, `DreamNote`, `motif` models.
- Telegram assistant retrieval tool behavior.
- External cultural research augmentation.

## Implementation Timing

- T13 adapts ingestion, chunking, embedding, migrations, and seeded fixture patterns.
- T14 adapts query-time retrieval, evidence assembly, `insufficient_evidence`, hybrid FTS/vector search, and stale index health.
- T22 adapts `scripts/eval.py`, eval doc update mechanics, CI eval tests, and regression thresholds.
