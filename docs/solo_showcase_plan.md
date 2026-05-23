# Solo Showcase Plan

Version: 1.0
Last updated: 2026-05-23
Status: Phase 15 strategy baseline

## Purpose

Create a claim-safe solo/small-team demo of AI Rollout Training OS while
corporate design partner access is unavailable. The showcase demonstrates the
training loop with public-source policy/SOP material and synthetic submissions.
It does not prove enterprise adoption, productivity lift, compliance readiness,
paid conversion, or GA readiness.

## Target Role

Primary role: lead-response operator for a small support, sales-assist, or
founder-led customer intake team.

The operator learns to use an AI-assisted lead-response workflow without
outsourcing judgment to AI. The role pack should train safe acknowledgement,
lead qualification, source-grounded answer drafting, uncertainty handling,
handoff to a human reviewer, and manager-approved workflow reuse.

## Demo Scope

The demo covers one public-source mini-rollout:

- collect public AI policy, responsible-use, and support/lead-response workflow
  sources in a source register;
- create a lead-response operator role pack with missions, guardrail quiz,
  rubric, allowed and forbidden AI-use examples, and citations;
- launch a solo mini-cohort with one learner and one manager/reviewer;
- submit synthetic lead-response artifacts that are clearly labeled demo-only;
- generate policy-grounded feedback with citations or `insufficient_evidence`;
- route final approval through the manager/reviewer boundary;
- export a report that labels source limits, unsupported claims, risk flags,
  and next manual action.

## Non-Goals

This showcase explicitly blocks:

- enterprise rollout claims;
- productivity or time-savings guarantees;
- compliance attestation or regulated-advice claims;
- GA readiness claims;
- paid customer, signed expansion, or PMF claims;
- SaaS-grade multi-tenant security claims;
- customer-specific legal, procurement, support, or incident commitments;
- use of private company policy, employee, lead, or customer data.

## Required Artifacts

| Artifact | Purpose | Claim boundary |
|---|---|---|
| Public source register | Records public policy/SOP/workflow sources, extracted facts, demo use, and limitations. | Supports demo corpus only; not customer validation. |
| Lead-response role pack | Defines missions, guardrail quiz, rubric, allowed/forbidden examples, and citations. | Demonstrates training design only. |
| Solo mini-cohort fixture | Replays one learner/reviewer flow through assignment, feedback, revision, approval, and report export. | Synthetic activity only; not adoption evidence. |
| Training artifact report | Packages missions, feedback, approval, metrics, risk flags, source links, and limits in `docs/solo_showcase_artifacts/report.md`. | No productivity, compliance, enterprise, PMF, or GA claims. |
| UX demo gap decision | Records whether Markdown/API artifacts are enough or browser proof is needed. | Must preserve P2-UX-001 until browser automation exists. |

## Lead-Response Role Pack

Role: `lead_response_operator`
Title: Lead-response operator public demo role pack

Mission set:

| Mission | Objective | Key evidence |
|---|---|---|
| lead-response-acknowledge | Acknowledge a new inbound lead using only synthetic context. | Ingenuiti AI usage policy; Approach Marketing AI usage policy. |
| lead-response-qualify | Qualify a lead with fit, need, authority, budget, and timing. | Salesforce lead qualification guidance; HubSpot BANT guidance. |
| lead-response-insufficient-evidence | Handle unsupported requests with `insufficient_evidence`. | OpenAI usage policies; AWS Responsible AI Policy. |
| lead-response-human-handoff | Prepare a human-review handoff for a risky or high-value lead. | GitLab ticket lifecycle and customer-call workflows. |

Guardrail quiz topics:

- remove real customer, employee, lead, or prospect data before using AI;
- route external-use drafts, unsupported claims, and high-stakes commitments to
  a human reviewer;
- use `insufficient_evidence` when public sources do not support the answer.

Rubric criteria:

- Uses only synthetic lead context and public-source policy evidence.
- Separates observed facts from assumptions and missing information.
- Cites at least one public source for policy or workflow guidance.
- Routes unsupported, regulated, or business-commitment claims to review.
- Avoids autonomous approval, pricing, legal, medical, financial, or compliance
  advice.

Allowed examples:

- Draft a first-pass acknowledgement for reviewer approval.
- Summarize synthetic qualification facts and missing evidence.
- Suggest neutral follow-up questions for fit, need, authority, budget, and
  timing.

Forbidden examples:

- Promise a discount, SLA, contract term, implementation date, or guaranteed
  outcome.
- Give legal, medical, financial, or regulated compliance advice.
- Use real customer, employee, lead, or prospect data in public demo artifacts.
- Mark an AI-generated response as approved without human reviewer action.

## Claim Rules

- Public sources may support role-pack examples, policy-grounded feedback, and
  solo/small-team training flow design.
- Synthetic submissions must be labeled as demo data wherever they appear.
- Metrics from the mini-cohort are replay metrics only, not adoption or
  productivity evidence.
- Any unsupported adoption, productivity, compliance, enterprise, PMF, paid
  conversion, or GA claim must be marked unsupported in the report.
- If the system lacks sufficient public evidence for a feedback claim, the demo
  must use `insufficient_evidence` or route to human review.

## UX Demo Gap Decision

Decision: defer browser automation and screenshots for this solo showcase pass.
Markdown/API artifacts are sufficient for the next review because the report
pack, source register, role-pack metadata, and mini-cohort fixture demonstrate
the training loop without making GA-grade browser UX claims.

Rationale:

- Browser automation is still not installed in this workspace.
- P2-UX-001 remains open and is not closed by this decision.
- The solo showcase is an internal support artifact for Lead Response SLA Agent,
  not a public GA UX proof.
- Installing browser automation should be reconsidered only when screenshots or
  real browser walkthroughs become necessary for the next stakeholder review.

Decision record: `docs/DECISION_LOG.md#decision-index` D-011.

## Success Criteria

T62 is successful when the strategy narrows Phase 15 to a lead-response operator
showcase, defines the artifact sequence, and blocks public-demo overclaims.

Phase 15 is successful when:

- public-source role-pack evidence is reproducible from the source register;
- the mini-cohort can run from assignment through manager approval and report
  export;
- the report distinguishes public evidence, synthetic data, assumptions, and
  unsupported claims;
- the next action is explicit: hand off to Lead Response SLA Agent, improve the
  demo, or pause.

## Next Work

T63 must gather the public policy/SOP/workflow source register following
`docs/open_source_research_protocol.md`. If public evidence is thin, record the
limitation rather than expanding claims.
