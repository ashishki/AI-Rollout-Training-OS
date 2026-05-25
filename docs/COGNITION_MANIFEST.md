# Cognition Manifest - AI Rollout Training OS

---
artifact_kind: retrieval_manifest
project: ai-rollout-training-os
source_repo: AI-Rollout-Training-OS
status: active
canonical: false
generated: false
tags: [training, rag, eval, cognition]
---

Version: 1.0
Last updated: 2026-05-25

## Purpose

Repo-local map for architectural memory, adoption hypothesis evidence, retrieval evals, and training-governance continuity.

## Authority Rules

- Canonical repo artifacts win over this manifest.
- Obsidian and generated indexes are optional navigation layers.
- Context packets must cite canonical paths before implementation or review relies on them.

## Project Identity

| Field | Value |
|-------|-------|
| Primary shape | Deterministic workflow plus text-only RAG and bounded LLM feedback |
| Governance level | Standard |
| Runtime tier | T1 |
| Active profiles | RAG, evaluation, governance/audit |

## Canonical Truth

| Surface | Path | Notes |
|---------|------|-------|
| Architecture | `docs/ARCHITECTURE.md` | Adoption OS design, RAG strategy, boundaries |
| Contract | `docs/IMPLEMENTATION_CONTRACT.md` | Implementation rules |
| Task graph | `docs/tasks.md` | Execution contract |
| Session state | `docs/CODEX_PROMPT.md` | Current baseline and open findings |
| Decisions | `docs/DECISION_LOG.md` | Decision index |
| Journal | `docs/IMPLEMENTATION_JOURNAL.md` | Cross-session continuity |
| Evidence | `docs/EVIDENCE_INDEX.md` | Proof lookup |
| Retrieval eval | `docs/retrieval_eval.md`, `tests/eval/test_retrieval_eval.py` | RAG quality memory |
| Feedback eval | `tests/eval/test_feedback_quality_eval.py`, `scripts/eval_feedback.py` | AI feedback quality |
| Audits | `docs/audit/` | Review history |

## Retrieval Scopes

| Scope | Start here | Include next |
|-------|------------|--------------|
| Strategist | `docs/ARCHITECTURE.md`, `docs/DECISION_LOG.md` | retrieval eval, pilot docs, audit findings |
| Orchestrator | `docs/CODEX_PROMPT.md`, `docs/tasks.md` | journal, evidence index, active evals |
| Implementer | current task, contract | task `Context-Refs`, affected tests/evals |
| Reviewer | contract, task ACs | evidence index, retrieval eval, prior audit phase |
| Eval regression | `docs/retrieval_eval.md` or feedback eval tests | evidence rows, task that changed retrieval/feedback |

## Known Gaps

| Gap | Impact | Migration step |
|-----|--------|----------------|
| No generated context packets committed | Review context is assembled manually | Generate packets for retrieval or feedback regressions only |
| Adoption hypothesis evidence is spread across pilot docs and evals | Strategist must search multiple files | Add evidence index rows for major pilot proof updates |

## Generated Artifacts

| Artifact | Path | Policy |
|----------|------|--------|
| Cognition index | `generated/cognition/index.json` | Optional generated artifact |
| Context packets | `docs/context-packets/` | Commit only major review/regression packets |

