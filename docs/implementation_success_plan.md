# Implementation Success Plan

Version: 1.0
Last updated: 2026-05-21
Owner: Implementation lead

This customer-facing plan describes how AI Rollout Training OS moves from
kickoff to expansion. It assumes the package tier, buyer, deployment option, and
success metrics are already aligned through `docs/packaging.md` and
`docs/procurement_packet.md`.

## Roles And Owners

| Role | Owner responsibilities |
|------|------------------------|
| Customer executive sponsor | Confirms business goal, package tier, budget owner, and expansion decision path. |
| Customer operator | Owns policy/SOP collection, role-pack review, cohort setup, and launch readiness. |
| Customer manager | Reviews learner work, approves reusable workflow changes, and validates success evidence. |
| Customer IT/security | Reviews SSO, deployment option, security packet, data processing, and incident contacts. |
| Implementation lead | Runs kickoff, project plan, configuration, readiness checks, and success review. |
| Product/operator support | Handles setup questions, issue triage, and runbook escalation. |

## Timeline

| Stage | Target timing | Exit evidence |
|-------|---------------|---------------|
| Kickoff | Week 0 | Buyer, scope, package tier, owners, deployment option, and success metrics confirmed. |
| Policy ingestion | Week 0-1 | Source documents imported, reviewed, and approved for retrieval use. |
| Role-pack setup | Week 1 | Role pack, missions, guardrail quiz, rubric, and manager review criteria approved. |
| Cohort launch | Week 1-2 | Learners enrolled, assignments created, reminders configured, and support path live. |
| Manager review | Week 2-3 | Manager queue reviewed, feedback quality sampled, and approved workflow changes tracked. |
| Reporting | Week 3-4 | Dashboard, pilot metrics, ROI assumptions, governance evidence, and report export reviewed. |
| Expansion review | Week 4 | Expand, repeat, pause, or reposition decision recorded with owners and next steps. |

## Kickoff

Customer responsibilities:
- Name executive sponsor, operator, manager reviewers, IT/security reviewer, and
  procurement contact.
- Confirm target team, learner count, role scope, and initial AI use cases.
- Confirm success metrics: activation, completion, guardrail pass rate, approved
  workflow changes, manager review SLA, risk rate, and expansion signal.

Implementation responsibilities:
- Confirm package tier and deployment option.
- Review procurement packet and security questions.
- Set the workspace, roles, SSO/OIDC path if needed, and integration choices.
- Document risks, open prerequisites, and launch date.

## Policy Ingestion

Customer responsibilities:
- Provide policy/SOP documents, allowed/forbidden use cases, approved examples,
  and manager approval rules.
- Identify document owners who can approve source snapshots.

Implementation responsibilities:
- Import documents through approved import path.
- Validate document type, ownership, and snapshot IDs.
- Require human approval before source snapshots become retrieval evidence.
- Record open gaps where policy is missing or ambiguous.

## Role-Pack Setup

Customer responsibilities:
- Approve role-pack goals, missions, guardrail quiz, rubric, and manager review
  criteria.
- Confirm which workflow changes require manager approval before reuse.

Implementation responsibilities:
- Configure role packs, missions, rubrics, guardrail quiz, and cohort draft.
- Verify learner instructions avoid sensitive-data entry.
- Confirm retrieval evidence and rubric feedback cite approved policy/SOP
  snapshots.

## Cohort Launch

Customer responsibilities:
- Confirm learner roster, manager assignments, launch message, and support
  contact.
- Confirm reminders and escalation expectations.

Implementation responsibilities:
- Launch cohort and verify assignments.
- Confirm learner access, guardrail quiz availability, submission path, and
  reminder configuration.
- Monitor activation, completion, feedback backlog, and sensitive-data flags.

## Manager Review

Customer responsibilities:
- Review submissions, feedback, risk flags, and workflow approval requests.
- Approve only workflow changes that are safe for reuse.
- Escalate legal, medical, financial, regulated, or policy-owner decisions to
  the appropriate human owner.

Implementation responsibilities:
- Monitor manager queue health and review SLA.
- Support feedback sampling/adjudication if Governance Plus is included.
- Record blockers, policy gaps, and training friction.

## Reporting

Customer responsibilities:
- Review pilot metrics, report export, approved workflow changes, risk signals,
  and customer-provided ROI assumptions.
- Confirm whether procurement or expansion evidence is sufficient.

Implementation responsibilities:
- Generate dashboard/report evidence.
- Run ROI calculator only with customer-provided assumptions.
- Prepare governance evidence or audit export if included in package tier.
- Summarize expand/repeat/pause/reposition options without guaranteed
  productivity claims.

## Expansion Review

Decision options:
- Expand when adoption, approved workflow changes, manager review SLA, risk
  controls, buyer ownership, and procurement path are strong.
- Repeat when the workflow is useful but evidence is incomplete.
- Pause when safety, quality, or buyer ownership is not ready.
- Reposition when value appears stronger in a different team, role, or buyer.

Required output:
- Decision, owner, target date, package tier, deployment option, next cohort,
  open risks, procurement steps, and support needs.

## Success Evidence Checklist

- Kickoff owners and success metrics recorded.
- Approved source documents and corpus versions recorded.
- Role pack, missions, guardrail quiz, and rubric approved.
- Cohort launched and learner access verified.
- Manager review queue used and approved workflow changes tracked.
- Dashboard, pilot metrics, ROI assumptions, and report export reviewed.
- Expansion decision recorded with owner and next step.
