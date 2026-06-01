# Ship It? Y/N Buyer Demo Readiness Review

Date: 2026-06-01
Scope: Phase 21 buyer-demo readiness after T98-T104
Status: SHOW_BUYER_DEMOS

## Summary

Ship It? Y/N is ready for bounded manual buyer demos and workshop discovery
conversations. The game is showable as a public permission-judgment experience
with a facilitator pack, safe aggregate summary path, local analytics, buyer
feedback template, scenario-authoring controls, and claim-boundary review.

This decision does not claim PMF, paid conversion, compliance approval,
certified safety, production readiness, incident reduction, customer adoption,
or real agent execution safety.

## Evidence Reviewed

| Area | Evidence | Result |
|---|---|---|
| Game route | `/demo/ship-it-yn`, `frontend/app_shell.py`, `tests/test_permission_game_public_demo.py` | PASS: local FastAPI route serves the built React/Vite game as a public demo. |
| Scenario coverage | `ai_rollout_os/permissions/game_scenarios/`, `tests/test_permission_game_scenarios.py`, `docs/permission_game_scenario_schema.md` | PASS: seven synthetic levels cover permission boundaries, risk categories, choices, inspect artifacts, feedback, badges, and facilitator notes. |
| Scoring | `ai_rollout_os/permissions/game_scoring.py`, `tests/test_permission_game_scoring.py` | PASS: deterministic scoring covers correct, partial, unsafe, and overblock outcomes with meter totals, badges, final title, and safe share text. |
| Browser evidence | `tests/browser/test_ship_it_yn_gameplay.py`, `tests/browser/test_ship_it_yn_accessibility.py`, `tests/browser/test_ship_it_yn_visual.py`, `docs/audit/artifacts/ship_it_yn_desktop.png`, `docs/audit/artifacts/ship_it_yn_mobile.png` | PASS: browser tests cover gameplay, accessibility basics, responsive framing, screenshots, same-origin resources, and no tracking network calls. |
| Facilitator pack | `docs/ship_it_yn_facilitator_pack.md`, `tests/test_ship_it_yn_workshop_pack.py` | PASS: workshop guidance maps all seven levels to lessons, discussion prompts, team risk hotspots, and no-shame facilitation rules. |
| Safe team summary | `ai_rollout_os/permissions/game_summary.py`, `tests/test_ship_it_yn_team_summary.py` | PASS: aggregate-only summary avoids personal ranking, raw prompts, code, credentials, customer data, personal identifiers, and shame mechanics. |
| Buyer feedback template | `docs/ship_it_yn_buyer_feedback.md`, `tests/test_ship_it_yn_buyer_feedback.py` | PASS: manual demo template captures buyer role, team agent usage, strongest/weakest scenario, workshop willingness, objections, next action, and observed-vs-assumed evidence. |
| Claim boundary review | `docs/audit/SHIP_IT_YN_CLAIM_BOUNDARY_REVIEW.md`, `tests/test_ship_it_yn_claim_boundary_review.py` | PASS: `CLAIM_BOUNDARY_PASS` blocks unsupported compliance, certified safety, production readiness, incident reduction, PMF, paid conversion, customer adoption, autonomous approval, and real execution claims. |

## Decision

Decision: SHOW_BUYER_DEMOS

Proceed to show buyer demos manually with tight claim boundaries:

- use the local route `/demo/ship-it-yn`;
- frame the demo as a permission-judgment game and workshop wedge;
- collect feedback in `docs/ship_it_yn_buyer_feedback.md` format;
- separate observed buyer evidence from founder/operator assumptions;
- stop or reposition if buyers do not recognize the workflow risk or cannot
  name a credible workshop audience.

## Claim Boundaries

- No PMF claim.
- No paid conversion claim.
- No compliance approval claim.
- No certified safety claim.
- No production readiness claim.
- No incident reduction claim.
- No autonomous permission approval claim.
- No real agent execution safety claim.

Allowed language:

- "Ready to show buyer demos manually."
- "Ready to test whether buyers recognize the permission-judgment problem."
- "Ready to collect observed feedback and objections."
- "Ready to use workshop interest as a discovery signal."

## Manual Demo Run Rules

1. Build the frontend and serve the FastAPI route locally.
2. Play one full seven-level run or a shorter scenario subset based on buyer
   role.
3. Ask which scenario felt strongest and weakest.
4. Ask whether the buyer would run a team workshop and why.
5. Capture objections, current workaround, and next action.
6. Record assumptions separately from observed buyer statements.
7. Do not store personal data, raw prompts, customer artifacts, credentials, or
   proprietary workflow text.

## Exit Criteria For The Next Human Loop

After three manual buyer demos:

- continue if buyers name the same workflow risk and agree to a workshop or
  scenario-customization next step;
- improve the game if buyers like the problem but find scenarios unclear or
  mismatched;
- pause or reposition if buyers do not use agents, do not own the problem, or
  cannot identify an urgent team workflow.
