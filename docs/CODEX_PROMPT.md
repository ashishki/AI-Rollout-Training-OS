# AI Rollout Training OS - Compact Session State

Version: 2.2
Date: 2026-06-01
Status: active-pivot

Full historical prompt archived at
`docs/archive/portfolio-cleanup-2026-05-29/CODEX_PROMPT_full_2026-05-29.md`.

## Current State

- Current phase: Phase 18 - Scenario And Scoring Core.
- Active pivot: polished React/Vite permission mini-game built on the Agent
  Permission Training Simulator.
- Reference direction: beautiful, convenient, showable, monetizable
  permission-judgment game with terminal-style interaction, risk meters,
  inspect/diff, sandbox, scope, eval, escalation, final report, and browser
  evidence.
- Active task source: Post-MVP production maturity graph,
  `docs/product_maturity_task_graph.md`.
- Phase status: Phase 16 readiness review complete; Phase 17 planning docs are
  complete through T78; Phase 18 implementation is complete through T83. Local browser
  demo route remains available at `/demo/permission-simulator`, with a captured
  Chrome screenshot at
  `docs/audit/artifacts/permission_simulator_demo.png`.
- Baseline: 207 passing tests (`.venv/bin/python -m pytest -q`, local Docker
  Postgres with test credentials).
- Lint baseline: `.venv/bin/ruff check` passes; `.venv/bin/ruff format --check`
  passes.

## Active Inputs

- `README.md`
- `docs/PROJECT_PLAN.md`
- `docs/product_maturity_roadmap.md`
- `docs/product_maturity_task_graph.md`
- `docs/IMPLEMENTATION_CONTRACT.md`
- `docs/ship_it_yn_product_spec.md`
- `docs/permission_game_scenario_schema.md`
- `docs/ship_it_yn_frontend_architecture.md`
- `docs/ship_it_yn_ai_development_plan.md`

## Product Direction

The v1 product is the Agent Permission Training Simulator. It teaches teams to
judge AI agent requests through visual scenarios, consequence feedback, scoring,
safer alternatives, and lesson text.

The next public product surface is Ship It? Y/N: a React/Vite/TypeScript/
Tailwind terminal-style game served from FastAPI at `/demo/ship-it-yn`.
It must be polished and convenient, not a compressed quiz. It should include
seven levels, inspect/diff mechanics, risk meters, deterministic scoring,
badges, final report, share text, and browser evidence.

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
- `T75-T78 planning package` completed on 2026-05-31 for Ship It? Y/N product
  spec, scenario schema, frontend architecture, and AI development plan.
- `T79: Game Scenario Pydantic Schema` completed on 2026-06-01.
- `T80: Seven Starter Game Scenarios` completed on 2026-06-01.
- `T81: Game Scoring Engine` completed on 2026-06-01.
- `T82: Meter And Badge Model` completed on 2026-06-01.
- `T83: Local Game Session Model` completed on 2026-06-01.

## Next Task

Active next task: T84: Scenario Safety Guard Tests.

## Open Findings

| ID | Severity | Status | Notes |
|----|----------|--------|-------|
| P2-UX-001 | P2 | Partial | Public permission simulator screenshot and capture script exist; Phase 20 must add browser e2e and screenshots for `/demo/ship-it-yn`, while broader app-shell browser e2e remains open before full UX readiness claims. |

## Fix Queue

- Complete T75-T105 for Ship It? Y/N before expanding into LMS or enterprise
  dashboards.

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
| 2026-05-31 | T75-T78 planning package | Added Ship It? Y/N product spec, scenario schema, React/Vite frontend architecture, AI development plan, and Phase 17-21 task graph. Next implementation task is T79. |
| 2026-06-01 | T79: Game Scenario Pydantic Schema | Added Pydantic scenario models for Ship It? Y/N records with validation coverage for choices, risks, feedback, levels, meters, badges, and facilitator notes. Next implementation task is T80. |
| 2026-06-01 | T80: Seven Starter Game Scenarios | Added seven JSON scenario records for Ship It? Y/N and validation coverage for level order, titles, feedback, outcomes, facilitator notes, badges, and audit events. Next implementation task is T81. |
| 2026-06-01 | T81: Game Scoring Engine | Added deterministic per-decision scoring for Ship It? Y/N outcomes, feedback, score deltas, safety deltas, meter deltas, and audit events. Next implementation task is T82. |
| 2026-06-01 | T82: Meter And Badge Model | Added deterministic session meter totals, badges, final titles, strongest habit, weakest risk area, and share text that does not reward unsafe speed. Next implementation task is T83. |
| 2026-06-01 | T83: Local Game Session Model | Added public-safe localStorage session projection with session id, scenario order, decision outcomes, inspected artifact ids, elapsed time, meter totals, badges, and final report fields while excluding raw/private data. Next implementation task is T84. |

## Rules

- Build a visual permission-judgment product, not a generic course.
- Ship It? Y/N must use React/Vite for the polished public game UI.
- Scenarios must teach boundaries: allowed, needs approval, blocked, unknown.
- Keep monetization small and concrete: workshop/demo pack before platform.
- Do not execute real commands, read real local files, request real credentials,
  or use live LLM scoring in the game.
