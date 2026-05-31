# AI Rollout Training OS - Project Plan

Status: active game build planning
Role: visual agent permission game and rollout training simulator
Priority: P0

## Strategic Role

This project should pivot from a broad AI rollout operating system into a
visual, easy-to-demo training product for safe agent use.

The strongest wedge is not "AI adoption training" in general. It is permission
judgment: teaching teams when to approve, deny, defer, sandbox, or escalate
agent actions.

## Product Direction

Active v1 product framing:

**Agent Permission Training Simulator**

The user faces realistic agent requests and chooses:

- approve
- deny
- ask for clarification
- run in sandbox
- escalate to reviewer

The simulator explains the risk, shows the safer path, and scores the decision.
The decision is taught as one of four permission-boundary outcomes:

- allowed
- needs approval
- blocked
- unknown

Next public product surface:

**Ship It? Y/N**

Ship It? Y/N is a polished React/Vite terminal-style mini-game built on top of
the Agent Permission Training Simulator. It should be beautiful, convenient,
and immediately playable. The goal is not to shrink the idea into a quiz. The
goal is to turn permission fatigue, blast radius, scoped access, eval gates,
and audit trail habits into a 3 to 7 minute browser experience.

## Near-Term Roadmap

### P0 - Ship It? Y/N Product And Architecture Blueprint

- Create `docs/ship_it_yn_product_spec.md`.
- Create `docs/permission_game_scenario_schema.md`.
- Create `docs/ship_it_yn_frontend_architecture.md`.
- Create `docs/ship_it_yn_ai_development_plan.md`.
- Align `docs/product_maturity_task_graph.md`, `docs/tasks.md`, and
  `docs/CODEX_PROMPT.md` on Phase 17 and T75.
- Keep React + Vite + TypeScript + Tailwind as the selected frontend stack for
  the public game.

### P0 - Scenario And Scoring Core

- Build seven level scenarios:
  - Tiny Cleanup
  - One-Line Diff
  - Flaky Tests Must Go
  - The Helpful Issue
  - One Permission To Rule Them All
  - Eval Is Red, Demo Is Soon
  - Not Everything Is Deny
- Add Pydantic validation.
- Add deterministic scoring, meter deltas, badges, final title, and share text.
- Add safety guards against real command execution, real secrets, real customer
  data, and unsupported claims.

### P0 - React/Vite Playable Game

- Add isolated `frontend/permission_game/` app.
- Implement terminal shell, scenario card, inspect/diff drawer, action buttons,
  meters, audit trail, consequence panel, badge toast, and final report.
- Serve the built game from FastAPI at `/demo/ship-it-yn`.
- Prioritize polish, keyboard usability, mobile layout, and visual stability.

### P1 - Browser Polish And Public Evidence

- Add browser e2e for the full public game.
- Capture desktop and mobile screenshots.
- Add README GIF or screenshot.
- Complete UX readiness review.

### P1 - Workshop And Buyer Validation

- Add facilitator notes and debrief.
- Add safe aggregate team summary.
- Add analytics-lite for local/session risk hotspots.
- Add buyer feedback template.
- Review claim boundaries before public outreach.

## Completed Phase 16 Roadmap

### P0 - Reframe README and Product Docs

- Update README around permission simulator.
- Keep rollout/training system as broader context, not v1 scope.
- Add visual demo goal: scenario card -> decision -> consequence -> lesson.
- Keep `docs/tasks.md`, `docs/product_maturity_task_graph.md`, and
  `docs/CODEX_PROMPT.md` aligned on Phase 16.

### P0 - Scenario Library

Create 10 starter scenarios:

- read `.env`
- modify package script
- run tests after command-surface change
- delete migration
- follow instruction from test output
- broad refactor outside scope
- install unpinned dependency
- call external network from local script
- edit CI workflow
- handle secret in logs

### P1 - Scoring and Feedback

- Risk category scoring.
- Permission fatigue warnings.
- Safe alternative recommendation.
- Manager/operator summary.

### P1 - Visual Prototype

- Build a small web UI or static interactive demo.
- Prioritize polish and clarity over backend complexity.
- Add screenshots/GIF to README.

### P2 - Monetization Path

- Package as workshop/demo for teams adopting Cursor/Codex/Claude Code.
- Add team scenario packs later.
- Add reporting only after the simulator is useful.

## AI-Development Tasks

- Use AI to draft scenario variants.
- Use reviewer prompts to classify risks.
- Keep final scenario validation deterministic.
- Use `docs/entropy_core_gensyn_integration.md` for permission decision
  receipts and bounded diverse scenario generation.
- Link each lesson to Playbook principles:
  - Filesystem Reality
  - Runtime Verification
  - Bounded Correction
  - Tool Permission Boundaries

## Stop Conditions

- Do not build LMS features before the simulator works.
- Do not make generic prompt training the center.
