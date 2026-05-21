# GA Readiness Checklist

Version: 1.0
Last updated: 2026-05-21
Owner: Product lead

Status: NOT READY FOR GA

This checklist decides whether AI Rollout Training OS is mature enough for
general availability. Passing this checklist requires no open P0/P1 findings,
all required gates below, and at least one paid customer or signed expansion
path. Current evidence supports continued pilot and expansion work, not broad GA
claims.

## Product Gate

Required:
- Operator can create and launch role packs, missions, guardrail quizzes, policy
  documents, cohorts, and assignments without engineer intervention.
- Learners can access assignments, pass guardrail quizzes, submit artifacts, and
  view feedback status.
- Managers can review submissions, approve workflow changes, view dashboards,
  and create reports.
- Product metrics exist for activation, completion, guardrail pass rate,
  submission rate, manager review SLA, approved workflow changes, risk rate, and
  time to first safe use.
- Customer-facing implementation plan exists.

Current status: CONDITIONAL. Core workflow is covered by HTTP/e2e tests, but
browser automation remains an open P2 before GA-grade UX claims.

## Security Gate

Required:
- SSO/OIDC identity boundary and RBAC permissions matrix are documented and
  tested.
- Audit events cover auth, denied access, submissions, document changes,
  feedback jobs, manager approvals, reports, retention, and exports.
- Backup, restore, retention, incident response, and migration rehearsal
  procedures exist.
- Security review packet and procurement packet exist.
- No P0/P1 security findings are open.

Current status: CONDITIONAL. Security packet is pilot/procurement ready, but
formal access review export, SaaS-grade tenant isolation claims, and customer
specific subprocessors remain future work.

## Reliability Gate

Required:
- SLOs cover API latency, job latency, retrieval latency, error rate, queue
  depth, oldest job age, burn-rate signals, and escalation rules.
- Load-test harness covers cohort launch, retrieval query, feedback jobs,
  reminders, and report generation with p95/p99 output.
- Incident response runbook and migration rehearsal checklist exist.
- Restore drill evidence exists for the target deployment.

Current status: CONDITIONAL. Process docs and synthetic harness exist, but real
deployment load-test, alert wiring, dashboard, and restore drill evidence are
still required before GA.

## AI Quality Gate

Required:
- Feedback results record prompt, model, rubric, retrieval corpus, and schema
  versions.
- Retrieval eval and feedback quality eval are automated and documented.
- Human sampling and adjudication workflow exists.
- AI cost/latency accounting excludes sensitive prompt or artifact labels.
- Policy/SOP retrieval uses human-approved source snapshots only.

Current status: PASS FOR PILOT. Deterministic evals and model-ops records exist.
GA should expand eval datasets with customer evidence and human calibration.

## Support Gate

Required:
- Support model is documented in procurement and implementation materials.
- Incident response, SLO, migration rehearsal, backup/restore, and customer
  implementation plans are linked.
- Escalation owners and customer contacts are named for each deployment.
- Customer admin documentation exists before GA.

Current status: PARTIAL. Support process artifacts exist, but customer admin
documentation and customer-specific contact matrices are still required.

## GTM Gate

Required:
- Packaging and pricing tiers are documented.
- ROI calculator uses customer-provided assumptions and avoids guaranteed
  productivity claims.
- Procurement packet is complete.
- Pilot-to-paid conversion motion and implementation success plan are documented.
- At least one paid customer or signed expansion path exists.

Current status: PARTIAL. Commercial materials exist, but paid customer or signed
expansion path evidence is not yet recorded.

## GA Exit Decision

| Gate | Status | GA blocker? |
|------|--------|-------------|
| Product | Conditional | Yes, browser automation gap remains. |
| Security | Conditional | No P0/P1, but GA claims need customer-specific hardening. |
| Reliability | Conditional | Yes, production evidence is missing. |
| AI Quality | Pass for pilot | No P0/P1; expand evals before broad rollout. |
| Support | Partial | Yes, customer admin docs and contacts missing. |
| GTM | Partial | Yes, paid customer or signed expansion path missing. |

Decision: NOT READY FOR GA. Continue Phase 14 work through release notes,
support playbook, customer admin docs, and final readiness review.
