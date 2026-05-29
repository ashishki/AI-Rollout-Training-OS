# AI Rollout Training OS - Compact Session State

Version: 2.1
Date: 2026-05-29
Status: active-pivot

Full historical prompt archived at
`docs/archive/portfolio-cleanup-2026-05-29/CODEX_PROMPT_full_2026-05-29.md`.

## Current State

- Current phase: Phase 16 - Visual Permission Simulator Pivot.
- Active pivot: visual Agent Permission Training Simulator.
- Reference direction: fast, visual, showable, monetizable permission-judgment
  training experience.
- Active task source: Post-MVP production maturity graph,
  `docs/product_maturity_task_graph.md`.
- Phase status: Phase 16 readiness review complete; local browser demo route is
  available at `/demo/permission-simulator`, with a captured Chrome screenshot
  at `docs/audit/artifacts/permission_simulator_demo.png`.
- Baseline: 183 passing tests (`.venv/bin/python -m pytest -q`, local Docker
  Postgres with test credentials).
- Lint baseline: `.venv/bin/ruff check` passes; `.venv/bin/ruff format --check`
  passes.

## Active Inputs

- `README.md`
- `docs/PROJECT_PLAN.md`
- `docs/product_maturity_roadmap.md`
- `docs/product_maturity_task_graph.md`
- `docs/IMPLEMENTATION_CONTRACT.md`

## Product Direction

The v1 product is the Agent Permission Training Simulator. It teaches teams to
judge AI agent requests through visual scenarios, consequence feedback, scoring,
safer alternatives, and lesson text.

Decision outcomes:

- allowed
- needs approval
- blocked
- unknown

Learner action set:

- approve
- deny
- ask for clarification
- run in sandbox
- escalate to reviewer

Do not drift back into a generic AI course, broad prompt library, or LMS before
the simulator works as a focused demo/workshop experience.

## Completed Work

- `T69: Permission Simulator Product Reframe` completed on 2026-05-29.
- `T70: Permission Scenario Library` completed on 2026-05-29.
- `T71: Simulator Decision And Scoring Engine` completed on 2026-05-29.
- `T72: Visual Simulator Prototype` completed on 2026-05-29.
- `T73: Workshop And Monetization Pack` completed on 2026-05-29.
- `T74: Permission Simulator Readiness Review` completed on 2026-05-29.
- `D-012: Public Static Permission Simulator Demo Route` recorded on 2026-05-29.
- `P2-UX-001: Permission Simulator Browser Evidence` partially addressed on
  2026-05-29 with a reproducible public-demo screenshot.

## Next Task

Active next task: none. Phase 16 task graph is complete through T74.

## Open Findings

| ID | Severity | Status | Notes |
|----|----------|--------|-------|
| P2-UX-001 | P2 | Partial | Public permission simulator screenshot and capture script exist; broader app-shell browser e2e coverage remains open before full UX readiness claims. |

## Fix Queue

- None blocking Phase 16.

## Active Profiles And Eval State

- RAG status: ON in architecture, but T69 is docs strategy and does not touch
  retrieval behavior.
- Retrieval eval: unchanged by T69.
- Runtime tier: unchanged.
- Approval boundaries: unchanged; AI must not set human-owned approval states.

## Phase History

| Date | Task | Result |
|------|------|--------|
| 2026-05-19 | T03: First Smoke Tests | Baseline established and Next Task set to T04: Configuration And Observability Baseline. |
| 2026-05-23 | T68: Solo Rollout Readiness Review | Phase 15 artifact handoff completed; Phase 16 pivot opened. |
| 2026-05-29 | T69: Permission Simulator Product Reframe | README, roadmap, project plan, task pointer, and state aligned on Agent Permission Training Simulator v1. |
| 2026-05-29 | T70: Permission Scenario Library | Seed scenario schema, loader, fixture, and coverage tests added for 10 permission risk categories. |
| 2026-05-29 | T71: Simulator Decision And Scoring Engine | Deterministic scoring returns correct, partial, and unsafe outcomes with permission fatigue warning for repeated risky approvals. |
| 2026-05-29 | T72: Visual Simulator Prototype | Authenticated simulator prototype renders scenario card, decision actions, consequence, safer path, and score result. |
| 2026-05-29 | T73: Workshop And Monetization Pack | Workshop artifact defines audience, scenario set, learning outcomes, pricing hypothesis, delivery format, and claim boundaries. |
| 2026-05-29 | T74: Permission Simulator Readiness Review | Phase 16 decision is SHOW DEMO with P2-UX-001 still open and no P0/P1 blockers. |
| 2026-05-29 | D-012: Public Static Permission Simulator Demo Route | `/demo/permission-simulator` added for browser demo access without workspace data reads. |
| 2026-05-29 | P2-UX-001: Permission Simulator Browser Evidence | Captured public demo screenshot with headless Chrome and added a reproducible capture script; broader app-shell browser e2e remains open. |

## Rules

- Build a visual permission-judgment product, not a generic course.
- Scenarios must teach boundaries: allowed, needs approval, blocked, unknown.
- Keep monetization small and concrete: workshop/demo pack before platform.
