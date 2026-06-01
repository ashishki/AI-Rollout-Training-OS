# Ship It? Y/N UX Readiness Review

Date: 2026-06-01
Scope: Phase 20 Ship It? Y/N browser polish and public demo evidence after T92-T97
Status: SHOW_PUBLIC_DEMO

## Summary

Ship It? Y/N is ready for bounded public demos and workshop conversations.

The public game is served at `/demo/ship-it-yn`, has validated scenario and
scoring coverage, builds as a React/Vite UI, has browser-level e2e coverage,
has durable desktop and mobile screenshots, and now has README first-screen
positioning with explicit claim boundaries. This is not a production-agent
approval system, compliance certificate, LMS, or PMF proof.

## Evidence Reviewed

| Area | Evidence | Result |
|---|---|---|
| Public route | `frontend/app_shell.py`, `tests/test_permission_game_public_demo.py`, `tests/test_permissions_matrix.py` | PASS: `/demo/ship-it-yn` serves the built Vite shell publicly with no auth or workspace data reads. |
| Scenario coverage | `ai_rollout_os/permissions/game_scenarios/`, `tests/test_permission_game_scenarios.py` | PASS: seven starter levels cover validated choices, risk categories, boundaries, inspect artifacts, feedback, badges, and facilitator notes. |
| Scoring and final report | `ai_rollout_os/permissions/game_scoring.py`, `tests/test_permission_game_scoring.py`, `frontend/permission_game/src/components/ResultScreen.tsx` | PASS: deterministic outcomes, meter deltas, badges, safe share text, and final-report fields are covered. |
| React/Vite UI | `frontend/permission_game/`, `frontend/permission_game/src/components/TerminalLayout.tsx`, component tests | PASS: terminal layout, scenario card, decisions, inspect drawer, meters, audit trail, consequence panel, badge toast, and final report are implemented. |
| Browser e2e | `tests/browser/test_ship_it_yn_gameplay.py` | PASS: Chrome DevTools test plays all seven levels, uses inspect/scope/eval/escalate/sandbox decisions, reaches final report, and checks same-origin local resources only. |
| Screenshots | `docs/audit/artifacts/ship_it_yn_desktop.png`, `docs/audit/artifacts/ship_it_yn_mobile.png`, `scripts/capture_ship_it_yn_demo.py`, `tests/test_permission_game_browser_artifacts.py` | PASS: desktop and mobile PNG artifacts were captured from the live route and are reproducible. |
| README visual and pitch | `README.md`, `tests/test_permission_game_marketing.py` | PASS: README presents Ship It? Y/N as the public permission judgment game, includes CTA, route, artifacts, target users, and blocked claims. |
| Claim boundaries | `README.md`, `tests/test_permission_game_marketing.py`, `tests/test_permission_game_safety.py` | PASS: No certified safety, compliance approval, production readiness, LMS, real agent runner, PMF, paid conversion, customer adoption, or autonomous execution claim is made. |

## Readiness Checks

| Check | Status | Notes |
|---|---|---|
| Browser-accessible public demo | PASS | `/demo/ship-it-yn` is reachable after building `frontend/permission_game/dist`. |
| Real browser proof | PASS | Browser e2e and durable screenshots exist. |
| Responsive and accessibility basics | PASS | T93/T94 browser and CSS tests cover desktop/tablet/mobile screenshots, reduced motion, focus states, keyboard shortcuts, reset, and share controls. |
| Public positioning | PASS | README first screen makes Ship It? Y/N the entry point and states non-goals. |
| Secrets and real execution | PASS | Game fixtures and browser tests avoid secrets, real command execution, local file reads, auth token requirements, and external tool calls. |
| Production readiness | NOT CLAIMED | Demo evidence supports showing the game, not production-agent infrastructure. |
| Buyer validation | NOT YET | Phase 21 must add facilitator pack, safe team summary, analytics lite, and buyer feedback loop before stronger GTM claims. |

## P2-UX-001 Status Update

| Finding | Previous status | Public game status | Remaining scope |
|---|---|---|---|
| P2-UX-001 | Partial | Resolved for Ship It? Y/N public game scope | Broader app-shell browser e2e remains open before full-platform UX readiness claims. |

## Accepted Limits

- Public demo readiness is scoped to Ship It? Y/N, not the full training OS.
- Screenshots are static evidence; they do not prove buyer adoption.
- Browser e2e covers local same-origin demo resources, not deployed hosting.
- No customer data, real policy authority, compliance approval, certified safety,
  production readiness, PMF, paid conversion, or customer adoption claim is made.

## Decision

Show public demo.

Proceed to Phase 21 workshop, analytics, and buyer validation.

Next task: `T99: Facilitator Debrief Pack`.
