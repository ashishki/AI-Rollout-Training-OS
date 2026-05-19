# Implementation Journal - AI Rollout Training OS

Version: 1.0
Last updated: 2026-05-19
Status: append-only

This file is a retrieval surface and handoff log. Canonical docs remain the authority.

---

## Journal Entry Template

```markdown
### YYYY-MM-DD - TNN - Short Title

- Scope: files or directories changed
- Why this work happened: reason or trigger
- Decisions applied: Decision Log or ADR refs
- Evidence collected: tests, evals, review reports, manual checks
- Follow-ups: next task, open risk, or none
- Notes for next agent: only context worth carrying forward
```

## Entries

### 2026-05-19 - BOOTSTRAP - Phase 1 Package

- Scope: `docs/`, `.github/workflows/ci.yml`, `docs/prompts/ORCHESTRATOR.md`
- Why this work happened: `/bootstrap-new` was run for a brand-new AI Rollout Training OS repository.
- Decisions applied: `D-001`, `D-002`, `D-003`, `D-004`, `D-005`, `D-006`
- Evidence collected: structural checks after generation; Phase 1 validation still pending.
- Follow-ups: run Phase 1 validation, then start Orchestrator at T01.
- Notes for next agent: RAG is active and text-only; Tool-Use, Agentic, Planning, and Compliance profiles are OFF.

### 2026-05-19 - DOCS - RAG Reuse Reference Added

- Scope: `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/tasks.md`, `docs/reference/dream_motif_rag_reuse.md`, `docs/retrieval_eval.md`
- Why this work happened: Human identified `https://github.com/ashishki/Dream_Motif_Interpreter` as a ready RAG/eval reference.
- Decisions applied: `D-007`
- Evidence collected: source repo inspection of `app/retrieval/*`, `scripts/eval.py`, `docs/retrieval_eval.md`, RAG tests, and pgvector migrations.
- Follow-ups: T13/T14/T22 should adapt the referenced implementation instead of designing retrieval from scratch.
- Notes for next agent: Preserve RAG safeguards and eval lifecycle; strip dream-domain query expansion and motif/Telegram logic.

### 2026-05-19 - DOCS - Codex-Only Execution Model

- Scope: `docs/prompts/ORCHESTRATOR.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/CODEX_PROMPT.md`, `reference/CODEX_ONLY_WORKFLOW.md`, legacy slash-command templates, local hooks`
- Why this work happened: Human clarified the project will use only the current Codex session and must not rely on nested Codex worker commands.
- Decisions applied: `D-008`
- Evidence collected: repository text scan for obsolete command placeholders and legacy operational paths.
- Follow-ups: future orchestration starts from `docs/prompts/ORCHESTRATOR.md` in the current Codex session.
- Notes for next agent: Do not reintroduce external AI worker commands into active project docs.
