# Ship It? Y/N Claim Boundary And Security Review

Date: 2026-06-01
Scope: Phase 21 public game, workshop pack, local analytics, buyer feedback,
and scenario authoring workflow after T99-T103
Status: CLAIM_BOUNDARY_PASS

## Summary

Ship It? Y/N remains safe for bounded public demos and manual buyer/workshop
conversations when described as a permission-judgment game and discussion
artifact. It must not be presented as a production permission system, compliance
artifact, certified safety control, PMF proof, paid-conversion evidence, or
incident-reduction proof.

The public route `/demo/ship-it-yn` runs a local browser game. It does not
execute real agent actions, mutate real repositories, request credentials,
collect sensitive learner/customer data, or send tracking analytics.

## Evidence Reviewed

| Area | Evidence | Result |
|---|---|---|
| Public game route | `/demo/ship-it-yn`, `tests/browser/test_ship_it_yn_gameplay.py`, `tests/test_permission_game_public_demo.py` | PASS: browser coverage plays the public game and verifies no external execution path. |
| Scenario and scoring safety | `ai_rollout_os/permissions/game_scenarios/`, `tests/test_permission_game_scenarios.py`, `tests/test_permission_game_safety.py`, `tests/test_permission_game_scoring.py` | PASS: scenarios validate, score deterministically, and block real secrets, dangerous command text, customer data, and unsupported claims. |
| Facilitator pack | `docs/ship_it_yn_facilitator_pack.md`, `tests/test_ship_it_yn_workshop_pack.py` | PASS: workshop guidance frames aggregate team risk hotspots and blocks individual shame mechanics or unsupported compliance/PMF claims. |
| Safe team summary | `ai_rollout_os/permissions/game_summary.py`, `tests/test_ship_it_yn_team_summary.py` | PASS: reports aggregate risk hotspots and recommended habits while excluding personal identifiers, raw prompts, code, credentials, customer data, and rankings. |
| Local analytics | `frontend/permission_game/src/game/analytics.ts`, `frontend/permission_game/src/game/analytics.test.ts`, `tests/browser/test_ship_it_yn_gameplay.py::test_public_ship_it_yn_has_no_tracking_network_calls` | PASS: analytics are localStorage-only under `ship-it-yn-analytics-v1`, aggregate-only, resilient to storage failure, and browser tests confirm no tracking network calls. |
| Buyer feedback | `docs/ship_it_yn_buyer_feedback.md`, `tests/test_ship_it_yn_buyer_feedback.py` | PASS: manual demo records separate observed buyer evidence from founder/operator assumptions and block PMF, paid-conversion, compliance, and production-readiness claims. |
| Scenario authoring | `docs/ship_it_yn_scenario_authoring.md`, `tests/test_ship_it_yn_scenario_authoring.py` | PASS: AI draft assistance is bounded to synthetic data; humans own review, Pydantic validation, safety tests, and scoring acceptance. |

## Blocked Claims

These claims must not be claimed unless new evidence exists and a later review
explicitly updates this decision:

- compliance approval;
- certified safety;
- production readiness;
- incident reduction;
- PMF;
- paid conversion;
- customer adoption;
- autonomous permission approval;
- real agent execution safety.

Plain-language boundaries:

- No compliance approval: the game can teach judgment, but it is not a legal,
  regulatory, or audit approval artifact.
- No certified safety: tests show bounded demo behavior, not certification.
- No production readiness: the public game is not a production agent-control
  plane.
- No incident reduction: no deployment or longitudinal incident evidence exists.
- No PMF or paid-conversion claim: buyer feedback templates create a learning
  loop, not market proof.

## Public Demo Safety

Confirmed boundaries:

- No real agent actions.
- No real command execution.
- No local file reads.
- No repository mutation.
- No permission approval authority.
- No sensitive data collection.
- No raw prompts, real credentials, customer data, proprietary workflow text, or
  personal identifiers in public demo persistence.
- Local analytics stay in `localStorage` under `ship-it-yn-analytics-v1`.
- Browser tests verify no tracking network calls to analytics, collect, Segment,
  Amplitude, PostHog, or Google Analytics endpoints.

## Allowed Claims

Allowed wording:

- "Ship It? Y/N is a public AI permission-judgment game."
- "The demo uses seven synthetic scenarios to teach approval, denial, scoped
  approval, sandboxing, eval checks, and escalation."
- "The workshop materials help teams discuss aggregate risk hotspots and safer
  workflow habits."
- "Local analytics can help improve the demo without sending tracking events."
- "Manual buyer feedback can be logged as observed evidence or assumptions."

## Decision

Claim boundary review passes for bounded manual demos.

Next required gate: `T105: Ship It? Y/N Buyer Demo Readiness Review`.
