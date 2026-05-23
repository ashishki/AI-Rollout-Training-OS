# Decision Log - AI Rollout Training OS

Version: 1.0
Last updated: 2026-05-23

This file is a retrieval index. Canonical documents win on conflict.

---

## Rules

- Keep entries short and link to the authoritative document or section.
- Record why a decision was made and what it replaced.
- Update this file when architecture, runtime, governance, or major implementation direction changes.
- Mark superseded decisions explicitly instead of deleting them.

## Decision Index

| ID | Date | Status | Decision | Why it matters | Canonical source | Supersedes |
|----|------|--------|----------|----------------|------------------|------------|
| D-001 | 2026-05-19 | Active | Use hybrid workflow shape with deterministic state and bounded LLM feedback. | Prevents drift into higher-autonomy agent behavior while preserving useful feedback generation. | `docs/ARCHITECTURE.md#solution-shape` | none |
| D-002 | 2026-05-19 | Active | Runtime tier is T1 with Docker Compose, PostgreSQL/pgvector, web process, and bounded worker. | Keeps early pilots deployable without shell mutation, privileged workers, or persistent autonomous runtime. | `docs/ARCHITECTURE.md#runtime-and-isolation-model` | none |
| D-003 | 2026-05-19 | Active | RAG profile is ON with text-only retrieval and index schema v1. | Company policies/SOPs must ground feedback and citations, but multimodal complexity is not justified for v1. | `docs/ARCHITECTURE.md#rag-architecture` | none |
| D-004 | 2026-05-19 | Active | Tool-Use, Agentic, Planning, and Compliance profiles are OFF for v1. | External calls are deterministic application code; no LLM-directed tools, autonomous loop, plan-primary product, or formal compliance attestation is needed yet. | `docs/ARCHITECTURE.md#capability-profiles` | none |
| D-005 | 2026-05-19 | Active | v1 assumes one company workspace per deployment. | Avoids premature SaaS tenancy claims while preserving `workspace_id` for later migration. | `docs/ARCHITECTURE.md#security-boundaries` | none |
| D-006 | 2026-05-19 | Active | Manager approval, certification, policy changes, and productivity claims remain human-owned. | Prevents adoption evidence from becoming unauditable AI authority. | `docs/ARCHITECTURE.md#human-approval-boundaries` | none |
| D-007 | 2026-05-19 | Active | Adapt RAG and retrieval evaluation from Dream Motif Interpreter. | Reuses a proven pgvector, hybrid FTS/vector retrieval, insufficient-evidence, and markdown eval pattern while requiring domain adaptation to policy/SOP evidence. | `docs/reference/dream_motif_rag_reuse.md` | none |
| D-008 | 2026-05-19 | Active | Use Codex-only orchestration with no external AI worker process. | The project will not use nested Codex worker commands; the current Codex session runs implementation, verification, review passes, and state updates directly. | `docs/prompts/ORCHESTRATOR.md` | none |
| D-009 | 2026-05-19 | Active | Run development as a nonstop Codex loop across phase boundaries. | Prevents idle handoff gaps; phase boundaries remain mandatory checks, but Codex continues to the next task/phase automatically when no blocker exists. | `docs/prompts/ORCHESTRATOR.md#phase-boundary` | none |
| D-010 | 2026-05-22 | Active | Prioritize a solo/small-team public-source rollout showcase before further enterprise or GA expansion. | The operator has limited corporate access, so the next useful proof is a claim-safe mini-cohort and role-pack demo that can support the Lead Response SLA Agent showcase. | `docs/product_maturity_task_graph.md#phase-15---solo-showcase-and-small-team-rollout`, `docs/open_source_research_protocol.md` | none |
| D-011 | 2026-05-23 | Active | Defer browser automation and screenshots for the solo showcase; use Markdown/API artifacts for this pass. | The showcase is an internal support artifact, not GA-grade UX proof. P2-UX-001 remains open until browser automation exists. | `docs/solo_showcase_plan.md#ux-demo-gap-decision` | none |

## Retrieval Notes

- Read this file before changing solution shape, runtime tier, profile status, retrieval mode, workspace model, or human approval boundaries.
- If a task has `Context-Refs`, prefer those scoped entries over scanning this file top-to-bottom.
