# Permission Simulator Readiness Review

Date: 2026-05-29
Scope: Phase 16 visual permission simulator after T69-T73
Decision: SHOW DEMO

## Summary

Phase 16 is ready for a small manual demo or workshop conversation. The work is
not ready for platform positioning, compliance claims, certified safety claims,
or production-agent approval claims.

The simulator now has a focused product frame, scenario coverage, deterministic
scoring, an authenticated visual prototype, and a workshop pack. This is enough
to show the concept and test willingness to pay for a service-led workshop.

## Evidence Reviewed

| Area | Evidence | Result |
|---|---|---|
| Scenario coverage | `tests/fixtures/permission_scenarios.json`, `tests/test_permission_scenarios.py` | PASS: 10 required risk categories are covered. |
| Scoring behavior | `ai_rollout_os/permissions/scoring.py`, `tests/test_permission_scoring.py` | PASS: scoring returns correct, partial, and unsafe outcomes with risk-specific feedback. |
| Visual prototype | `frontend/app_shell.py`, `ai_rollout_os/permissions/demo.py`, `tests/test_permission_ui.py` | PASS: authenticated UI renders scenario card, request, context, decision actions, consequence, safer path, and score result. |
| Workshop pack | `docs/permission_simulator_workshop_pack.md` | PASS: audience, scenario set, learning outcomes, pricing hypothesis, delivery format, and claim boundaries are explicit. |
| Product alignment | `README.md`, `docs/product_maturity_roadmap.md`, `docs/PROJECT_PLAN.md`, `docs/CODEX_PROMPT.md` | PASS: Phase 16 is framed as Agent Permission Training Simulator, not generic AI training. |
| Browser screenshot | `docs/audit/artifacts/permission_simulator_demo.png`, `scripts/capture_permission_simulator_demo.py`, `tests/test_permission_demo_browser_artifact.py` | PASS: public demo route renders in headless Chrome and produces a reproducible PNG artifact. |

## Readiness Checks

| Check | Status | Notes |
|---|---|---|
| Teaches permission boundaries | PASS | The product vocabulary covers allowed, needs approval, blocked, and unknown. |
| Covers realistic agent risks | PASS | Starter set includes secrets, command surfaces, test-output injection, package scripts, CI edits, out-of-scope refactors, network calls, deletes, dependency install, and log exposure. |
| Preserves approval boundary | PASS | Scoring and UI do not approve real privileged actions or set human-owned approval states. |
| Small monetization path | PASS | Workshop pack is service-led and small-ticket before platform expansion. |
| Browser proof | PARTIAL | Public demo screenshot and capture script now exist; P2-UX-001 remains open for broader browser-level e2e coverage before full UX readiness claims. |
| Production readiness | NOT CLAIMED | The artifact is not positioned as production-agent infrastructure. |
| Browser-accessible local demo | PASS | D-012 adds `/demo/permission-simulator` with static scenario content only; authenticated app routes remain protected. |

## Accepted Limits

- Demo scenario source in product code currently contains one prototype scenario;
  the broader seed library remains in the test fixture for T70/T71 coverage.
- Visual prototype is server-rendered HTML, not a polished standalone frontend.
- Browser proof is limited to one public demo screenshot, not a full browser e2e
  suite for all app-shell workflows.
- No customer-specific policy mapping exists.
- No real buyer validation, paid conversion, or workshop delivery evidence exists.

## Blocked Claims

Do not claim:

- certified safe AI use;
- compliance approval or regulated attestation;
- production readiness for autonomous agents;
- GA readiness;
- productivity, time-savings, or incident-reduction guarantees;
- customer security approval;
- PMF or paid conversion proof.

## Next Action

Show demo.

Use the current simulator and workshop pack for a bounded manual conversation
with a target team or buyer. The goal is to test whether agent permission
judgment is a strong enough wedge for a paid workshop/demo pack.

Local browser demo route: `/demo/permission-simulator`.

This public route is intentionally limited to static demo content and
deterministic scoring. It does not read workspace records, policy documents,
learner submissions, customer data, or user state.

Browser screenshot artifact: `docs/audit/artifacts/permission_simulator_demo.png`.
Reproduce it with:

```bash
APP_ENV=test .venv/bin/uvicorn ai_rollout_os.main:app --host 127.0.0.1 --port 8000
.venv/bin/python scripts/capture_permission_simulator_demo.py
```

Recommended demo script:

1. Show the scenario card and decision buttons.
2. Submit one risky request and review the consequence, safer path, and score.
3. Walk through the 10-category scenario set.
4. Show the workshop pack and pricing hypothesis.
5. Ask whether the team would pay for a facilitated version with custom
   scenarios from their actual agent surfaces.

Do not expand into LMS, dashboards, or enterprise procurement work until this
manual demo produces stronger buyer evidence.
