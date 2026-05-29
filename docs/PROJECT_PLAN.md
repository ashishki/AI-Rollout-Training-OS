# AI Rollout Training OS - Project Plan

Status: active pivot
Role: visual agent permission and rollout training simulator
Priority: P0

## Strategic Role

This project should pivot from a broad AI rollout operating system into a
visual, easy-to-demo training product for safe agent use.

The strongest wedge is not "AI adoption training" in general. It is permission
judgment: teaching teams when to approve, deny, defer, sandbox, or escalate
agent actions.

## Product Direction

New product framing:

**Agent Permission Training Simulator**

The user faces realistic agent requests and chooses:

- approve
- deny
- ask for clarification
- run in sandbox
- escalate to reviewer

The simulator explains the risk, shows the safer path, and scores the decision.

## Near-Term Roadmap

### P0 - Reframe README and Product Docs

- Update README around permission simulator.
- Keep rollout/training system as broader context, not v1 scope.
- Add visual demo goal: scenario card -> decision -> consequence -> lesson.

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
