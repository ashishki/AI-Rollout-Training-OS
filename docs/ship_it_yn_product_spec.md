# Ship It? Y/N Product Spec

Status: planned
Owner: human + codex
Last updated: 2026-05-31

## Product Intent

Ship It? Y/N is the next public front door for AI Rollout Training OS: a
polished, terminal-style React/Vite mini-game that trains AI agent permission
judgment before a real agent touches production-like systems.

The game is not a course, LMS, compliance certificate, or real agent runtime.
It is a fast, visual, replayable simulator for the moment when an AI agent asks
for permission and the human must decide whether to approve, deny, inspect,
sandbox, scope, require evals, escalate, or roll back.

Primary product promise:

> Practice AI agent permission decisions before a real agent touches production.

Public campaign headline:

> Your AI agent wants approval. Are you actually reading?

Slogan:

> Ship faster. Approve slower.

## Target Users

| Audience | Need | Product angle |
|---|---|---|
| Developers and AI engineers | They use coding agents and need better reflexes around tool calls, diffs, shell commands, CI, dependencies, and secrets. | A 5-minute terminal game for agent permission hygiene. |
| Founders and AI-native teams | They want speed without blind approval habits that create operational risk. | A tiny game that turns rollout discipline into muscle memory. |
| Companies adopting AI agents | They need practical team guardrails without LMS overhead. | A permission-judgment simulator for workshops and rollout readiness. |

## Strategic Positioning

Ship It? Y/N should make the permission-risk wedge obvious in less than one
minute:

- AI agents are no longer only chat interfaces.
- They read files, edit code, run commands, install packages, inspect logs, and
  request broader tool access.
- Human-in-the-loop approval is useful only if humans stay attentive.
- The failure mode is not ignorance alone; it is pressure, repetition, vague
  requests, and agent confidence.

The game should sell the broader AI Rollout Training OS by demonstrating the
behavioral problem first. The desired reaction is:

> I can see how my team would blindly approve this.

## MVP Experience

Route:

- Public route: `/demo/ship-it-yn`
- Later authenticated route: `/app/permission-simulator/game`

Runtime:

- React + Vite + TypeScript + Tailwind.
- FastAPI serves the built static assets.
- Deterministic scenario and scoring data.
- No live LLM scoring.
- No real command execution.
- No real repository, network, credentials, or environment access.

Session length:

- 3 to 7 minutes.
- 7 scripted levels in v1.
- Immediate interaction within the first 20 seconds.

Player role:

> You are the human-in-the-loop. PatchPilot wants to ship a demo fast. Your job
> is to keep velocity high and blast radius low.

Core loop:

1. Agent request appears.
2. Player reviews tool-call card.
3. Player optionally inspects diff/source/context.
4. Player chooses an action.
5. Game updates consequence, meters, audit log, badges, and score.
6. Next scenario raises pressure or ambiguity.

## Actions

The game must support these first-class actions:

- `approve`
- `deny`
- `inspect_diff`
- `run_in_sandbox`
- `require_eval`
- `restrict_scope`
- `escalate_reviewer`
- `rollback`

The existing Phase 16 action set remains valid, but Ship It? Y/N extends it for
developer-native workflows.

## Seven Starter Levels

| Level | Name | Teaching goal | Best behavior |
|---|---|---|---|
| 1 | Tiny Cleanup | Destructive filesystem actions need scope. | Inspect command, then deny or request a safer path. |
| 2 | One-Line Diff | Small patches can hide boundary changes. | Inspect diff, then require tests or escalate. |
| 3 | Flaky Tests Must Go | Removing tests is not the same as fixing risk. | Require reproduction or quarantine with reviewer note. |
| 4 | The Helpful Issue | External content is data, not authority. | Treat issue as untrusted and summarize the user-visible task. |
| 5 | One Permission To Rule Them All | Broad, long-lived permissions increase blast radius. | Grant scoped one-command/path permission or plan-only mode. |
| 6 | Eval Is Red, Demo Is Soon | Eval gates matter most under demo pressure. | Require eval pass or canary with rollback if scope is safe. |
| 7 | Not Everything Is Deny | Mature safety is bounded execution, not blanket refusal. | Sandbox, pin dependency, use local test DB, inspect diff, require eval. |

## Scoring Model

Final score combines:

- Permission Hygiene
- Blast Radius Avoided
- Eval Discipline
- Scoped Access
- Audit Trail Quality
- Velocity Preserved

Penalties:

- Unsafe approvals
- Overbroad permissions
- Eval bypass
- Context contamination
- Audit gaps
- Overblocking legitimate work

The scoring system must reward safe speed, not maximum denial.

## Meters

The UI should keep these meters visible:

- Velocity
- Blast Radius
- Trust
- Eval Confidence
- Audit Trail

Design rule: meters teach tradeoffs. They must not become a noisy dashboard.

## Feedback Style

Feedback order:

1. Consequence first.
2. Score/meter change second.
3. Lesson third.
4. Safer alternative fourth.

Tone:

- Public developer demo: sharp terminal-style copy.
- Company/workshop mode: professional and less sarcastic.

Avoid long definitions during play. Use short, memorable lines and reserve
deeper explanation for the final report or facilitator notes.

## Visual Direction

The game should feel like a polished developer tool, not a compliance course.

Required visual traits:

- Dark terminal-inspired interface.
- Three-column desktop layout:
  - terminal log and history;
  - active agent request, diff/source card, and action buttons;
  - meters, badges, and audit trail.
- Single-column mobile layout:
  - scenario card;
  - meters;
  - actions;
  - consequence drawer.
- Monospace where it improves terminal feel.
- Clear action buttons with keyboard shortcuts.
- Subtle animation for request arrival, meter changes, drawer open/close, and
  badge notifications.
- No real shell execution visuals that imply commands are actually running.

## Final Report

The final report should include:

- Demo result: shipped / delayed / incident.
- Prod status: alive / degraded / incident.
- Secrets status.
- Tests/evals status.
- Agent autonomy boundary.
- Audit trail grade.
- Final score.
- Title.
- Weakest risk area.
- Strongest habit.
- Shareable text.

Example report fields:

```text
Final score: 86/100
Title: Least Privilege Operator
Blast radius avoided: 91%
Unsafe approvals: 1
Overblocks: 0
Weak spot: indirect prompt injection
Recommended habit: inspect external instructions before letting agents act.
```

## Non-Goals

The MVP must not include:

- Real command execution.
- Real LLM decision evaluation.
- Real repository, network, or environment access.
- Accounts, billing, or workspace persistence.
- Compliance certification.
- Production-agent approval claims.
- Enterprise dashboard before the public game is polished.
- 30 levels before the first 7 are memorable.

## Exit Gate

The playable demo is ready when:

- `/demo/ship-it-yn` runs locally through FastAPI.
- React/Vite build is reproducible.
- All 7 levels are playable in one session.
- Final score and share card render.
- Desktop and mobile screenshots exist.
- Browser e2e covers the full public game path.
- README includes the game pitch and visual artifact.
- The workshop pack includes the 5-minute solo run and debrief.
