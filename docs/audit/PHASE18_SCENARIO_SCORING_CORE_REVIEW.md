# Phase 18 Scenario And Scoring Core Review

Date: 2026-06-01
Scope: Phase 18 Ship It? Y/N scenario and scoring core after T79-T84
Status: PASS

## Summary

Phase 18 is ready to hand off into Phase 19 React/Vite implementation.

The Ship It? Y/N core is now data-driven, deterministic, and bounded for a
public demo scaffold: scenario records validate through Pydantic, seven starter
levels exist, scoring is deterministic, session summaries are public-safe, and
scenario safety guard tests block secrets, dangerous command snippets, real
customer-data domains, and unsupported product claims.

This review does not claim the game is playable yet. It approves only the
scenario and scoring core for UI wiring.

## Evidence Reviewed

| Area | Evidence | Result |
|---|---|---|
| Scenario schema | `ai_rollout_os/permissions/game_schema.py`, `tests/test_permission_game_scenarios.py` | PASS: records validate ids, levels, tool calls, context, inspect artifacts, choices, feedback, meters, badges, audit events, and facilitator notes. |
| Starter levels | `ai_rollout_os/permissions/game_scenarios/`, `tests/test_permission_game_scenarios.py` | PASS: seven ordered Ship It? Y/N starter scenarios exist and validate. |
| Decision scoring | `ai_rollout_os/permissions/game_scoring.py`, `tests/test_permission_game_scoring.py` | PASS: decisions return outcome, consequence, lesson, safer alternative, score delta, safety delta, meter deltas, and audit events. |
| Meter and badge model | `ai_rollout_os/permissions/game_scoring.py`, `tests/test_permission_game_scoring.py` | PASS: session totals, badges, final titles, strongest habit, weakest risk area, and share text are deterministic and do not reward unsafe speed. |
| Public session model | `ai_rollout_os/permissions/game_session.py`, `tests/test_permission_game_scoring.py` | PASS: localStorage-safe state excludes actor/workspace ids, raw prompts, credentials, local files, customer data, and raw feedback text. |
| Scenario safety guards | `tests/test_permission_game_safety.py` | PASS: fixtures are scanned for secret-like values, real execution snippets, customer-data domains, and unsupported safety/compliance/PMF/conversion claims. |
| Existing receipt integration | `ai_rollout_os/permissions/proof.py`, `frontend/app_shell.py`, `tests/test_permission_proof_receipts.py`, `tests/test_permission_ui.py`, `docs/entropy_core_gensyn_integration.md` | PASS: the existing permission simulator result loop builds local receipt-compatible proof receipts after scoring. |

## Readiness Checks

| Check | Status | Notes |
|---|---|---|
| Data-driven game core | PASS | Scenario JSON is the source of scenario content; scoring consumes validated records. |
| Deterministic scoring | PASS | No live LLM scoring, random scoring, network calls, or command execution paths are present. |
| Permission teaching coverage | PASS | Starter set covers least privilege, diff inspection, eval gates, sandboxing, escalation, overbroad access, and overblocking. |
| Public demo data boundary | PASS | Session state stores summary decisions and report fields only, not raw scenario content or private workspace fields. |
| Claim boundary | PASS | Safety guards prevent fixtures from claiming certification, compliance approval, production safety, PMF, or paid conversion. |
| Receipt reuse boundary | PASS | Existing receipt builder is already wired to the current permission simulator loop. Ship It? Y/N should reuse it when the game has a result route or final report loop, not by duplicating receipt logic in the scoring core. |
| Phase 19 entry | PASS | T85 can start with the React/Vite scaffold and typed scenario import. |

## Accepted Limits

- The Ship It? Y/N React/Vite app does not exist yet.
- The public `/demo/ship-it-yn` route does not exist yet.
- The game has no browser evidence, screenshots, keyboard pass, or mobile
  visual proof yet; those remain Phase 20 work.
- Ship It? Y/N does not yet emit per-gameplay proof receipts because there is
  no game result loop to attach them to. The existing receipt builder must be
  reused later rather than reimplemented.
- No buyer validation, paid conversion, PMF, or workshop delivery evidence
  exists for Ship It? Y/N.

## Blocked Claims

Do not claim:

- playable public game;
- browser-polished UI;
- production readiness for autonomous agents;
- certified safety;
- compliance approval;
- GA readiness;
- productivity, time-savings, or incident-reduction guarantees;
- PMF or paid conversion proof.

## Open Findings

| ID | Severity | Status | Notes |
|---|---|---|---|
| P2-UX-001 | P2 | Partial | Permission simulator browser screenshot exists; Ship It? Y/N still needs browser e2e and screenshot evidence in Phase 20. |

## Decision

Proceed to Phase 19.

Next task: `T85: React/Vite Permission Game Scaffold`.
