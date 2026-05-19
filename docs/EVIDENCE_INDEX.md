# Evidence Index - AI Rollout Training OS

Version: 1.0
Last updated: 2026-05-19

This file indexes durable proof so agents can retrieve evidence quickly. It is not authoritative by itself. Every row must point to an actual artifact that carries the evidence.

---

## When To Use

Use this file because the project has active RAG evaluation artifacts, heavy tasks, and audit evidence needs.

## Evidence Table

| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |
|------------------------|---------------|----------|---------------|---------------|------------|
| Phase 1 architecture package | planning docs | `docs/ARCHITECTURE.md`, `docs/spec.md`, `docs/tasks.md`, `docs/IMPLEMENTATION_CONTRACT.md` | Initial solution shape, runtime, profile status, and task graph | 2026-05-19 | Yes |
| RAG evaluation lifecycle | eval | `docs/retrieval_eval.md` | Retrieval dataset, metrics, no-answer behavior, and evaluation history | 2026-05-19 | Yes |
| RAG implementation reuse | reference | `docs/reference/dream_motif_rag_reuse.md` | Source repo files and adaptation constraints for RAG ingestion, query, eval, and pgvector migrations | 2026-05-19 | No |
| Codex-only workflow | reference | `reference/CODEX_ONLY_WORKFLOW.md`, `docs/prompts/ORCHESTRATOR.md` | Active execution model excludes external AI worker commands | 2026-05-19 | Yes |
| Audit prompt set | review prompt | `docs/audit/` | Review cycle prompts and audit index | 2026-05-19 | Yes |
| Bootstrap handoff | journal note | `docs/IMPLEMENTATION_JOURNAL.md#entries` | Why the bootstrap package exists and next actions | 2026-05-19 | No |

## Retrieval Rules

- Prefer rows matching the current task's `Context-Refs`, open findings, or active profile tags.
- If an evidence row points to a stale or missing artifact, fix the artifact or remove the row.
- Do not treat a journal note as proof when a test, eval, or review report exists.
