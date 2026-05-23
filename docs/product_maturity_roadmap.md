# Product Maturity Roadmap

Version: 1.0
Date: 2026-05-19
Status: post-MVP planning artifact

This roadmap turns the current pilot-ready MVP into a mature production product.
It is written for the Codex-only AI loop and pairs with
`docs/product_maturity_task_graph.md`.

---

## Strategic Thesis

The product should not mature into a generic LMS. The durable market position is:

> AI adoption operating system for role-based enablement, policy-grounded
> feedback, and manager-approved workflow change.

The buyer pain is not "employees need prompt training." The higher-value pain is
that companies cannot prove AI adoption is safe, policy-aligned, role-specific,
measurable, and manager-governed.

## Target Market Wedge

- ICP: B2B SaaS, business services, or regulated-adjacent companies with active
  customer support teams.
- Initial buyer: VP Support, Enablement, RevOps, or AI Transformation lead.
- Internal blockers: Security, Legal, Compliance, IT, Procurement.
- First use case: support teams learning safe AI-assisted customer reply and
  workflow reuse.

Avoid broad horizontal positioning until 3-5 pilots prove repeated willingness
to pay.

## Maturity Principles

- Prove value before expanding surface area.
- Treat security, auditability, and governance as product features.
- Keep human approval boundaries explicit and tested.
- Make retrieval and feedback quality measurable before adding more AI behavior.
- Build enterprise integrations only after the core pilot loop is repeatable.
- Prefer single-tenant enterprise readiness before claiming SaaS-grade
  multi-tenancy.

## Phase Overview

| Phase | Name | Product Question | Exit Gate |
|-------|------|------------------|-----------|
| 6 | PMF Pilot System | Do target teams repeatedly complete missions and approve useful workflow changes? | 3 design partners complete pilots with measurable outcomes. |
| 7 | Core Product UX | Can a non-developer run the pilot flow end to end? | Admin/manager/learner UI covers role packs, cohorts, submissions, feedback, approvals, and reports. |
| 8 | Enterprise Security | Can IT/security approve a real deployment? | SSO/RBAC/audit/backup/tenant-boundary story passes a security review. |
| 9 | Governance Layer | Can legal/compliance trust the evidence trail? | Policy approvals, control mapping, risk taxonomy, and audit exports exist. |
| 10 | Integrations | Can the product fit into the customer's operating system? | Slack/Teams, HRIS/LMS, and knowledge-base ingestion are production-ready. |
| 11 | AI Quality & Model Ops | Can feedback quality survive model, prompt, and corpus changes? | Regression eval, prompt/model registry, quality dashboards, and human sampling are active. |
| 12 | Reliability & Scale | Can the product run for many teams without operator babysitting? | SLOs, monitoring, load tests, backup/restore, and incident runbooks exist. |
| 13 | Commercial Packaging | Can sales, security, and procurement close repeatable deals? | Pricing, packaging, ROI proof, security packet, and onboarding playbook are ready. |
| 14 | GA Readiness | Is the product mature enough for general availability? | GA checklist passes with no P0/P1 findings. |
| 15 | Solo Showcase And Small-Team Rollout | Can a solo operator show the training loop without corporate access? | Public-source role pack, mini-cohort, approval report, and claim-safe demo artifacts are ready. |

## Phase 6 - PMF Pilot System

Goal: prove the product solves a repeated business problem for a narrow ICP.

Build:

- Pilot outcome metrics: activation, completion, approved workflow changes,
  risk flags, manager review time, time-to-first-safe-use.
- Customer discovery and objection log.
- Pilot success rubric.
- Lightweight ROI model.
- Design partner reporting pack.

Phase 6 metrics:

| Metric | Source | Denominator |
|--------|--------|-------------|
| Activation rate | Stored guardrail quiz pass records for learners enrolled in the cohort | Enrolled learners |
| Completion rate | Stored mission assignment status records | Assigned missions |
| Approved workflow changes | Manager-approved submission records with approved workflow change text | Cohort |
| Manager review time | Stored submission created and manager approval timestamps | Manager-reviewed approved submissions |
| Risk rate | Stored sensitive-data flags and feedback risk flags | Cohort submissions |
| Time-to-first-safe-use | First stored clear submission from a learner with a passing guardrail result | Cohort start timestamp |

Phase 6 exit gate:

- At least 2 pilots show manager-approved workflow changes.
- At least 1 pilot has a credible path to paid expansion.
- Top 5 adoption blockers are documented with product responses.

## Phase 7 - Core Product UX

Goal: remove developer dependency from normal operations.

Build:

- Operator UI for policy documents, role packs, missions, guardrail quizzes,
  cohorts, and launches.
- Learner UI for assignments, guardrail quiz, submissions, feedback, and status.
- Manager UI for queue, filters, approval, dashboard, and reports.
- Empty states, errors, onboarding checklists, and activity timeline.

Exit gate:

- A non-engineer can run a pilot from policy upload to report export.
- End-to-end browser tests cover critical workflows.
- No workflow requires direct DB edits or curl scripts.

## Phase 8 - Enterprise Security

Goal: become deployable in serious enterprise environments.

Build:

- OIDC/SAML SSO.
- RBAC with explicit permissions matrix.
- Tenant isolation decision: single-tenant hardened deployment first, SaaS RLS
  only after ADR.
- Backup and restore procedures.
- Data retention and deletion workflows.
- Security questionnaire packet.

Exit gate:

- Security review packet exists.
- Backup/restore test passes.
- Access review export exists.
- No committed real secrets or sensitive data in logs/audits/reports.

## Phase 9 - Governance Layer

Goal: become part of the customer's AI governance stack.

Build:

- Policy approval workflow.
- Control mapping to internal AI policy and NIST AI RMF-style categories.
- Risk taxonomy and risk review lifecycle.
- Evidence lineage from source document to feedback to approval to report.
- Audit export package.

Exit gate:

- Legal/compliance can inspect why a feedback or approval happened.
- Governance exports are reproducible.
- Human-owned decisions cannot be automated by AI paths.

## Phase 10 - Integrations

Goal: fit into customer systems without duplicate administration.

Build:

- Slack/Teams reminders and manager alerts.
- HRIS/user import.
- LMS completion export.
- Knowledge-base ingestion from Google Drive, Confluence, Notion, SharePoint,
  or manual upload v2.
- Webhooks for downstream reporting.

Exit gate:

- Integrations are disabled by default and explicitly enabled.
- External calls are retried and audited.
- Integration failures do not corrupt durable product state.

## Phase 11 - AI Quality & Model Ops

Goal: make AI-assisted feedback measurable, explainable, and regression-safe.

Build:

- Golden eval datasets per role/customer.
- Prompt/model/version registry.
- Regression gate for retrieval and feedback quality.
- Human sampling and adjudication workflow.
- Cost and latency monitoring by model and feature.
- Provider abstraction and fallback plan.

Exit gate:

- Model or prompt changes cannot ship without eval comparison.
- No-answer behavior is measured.
- Feedback quality dashboard is visible to operators.

## Phase 12 - Reliability & Scale

Goal: run reliably for many teams and many cohorts.

Build:

- SLOs and service dashboards.
- Queue depth, job age, error rate, p95/p99 latency metrics.
- Load tests for cohort launch, retrieval query, feedback jobs, and reports.
- Incident response runbook.
- Data migration rehearsal.

Exit gate:

- Load test meets target pilot and expansion sizes.
- On-call runbook exists.
- Restore drill passes.

## Phase 13 - Commercial Packaging

Goal: make the product repeatably sellable.

Build:

- Packaging tiers: Team Pilot, Enterprise Enablement, Governance Plus,
  Regulated Single-Tenant.
- Pricing model based on active learners, role packs, governance features,
  integrations, and deployment model.
- ROI calculator.
- Security/procurement packet.
- Implementation success plan.

Exit gate:

- Sales can explain value in one page.
- Procurement can receive a complete packet.
- Pilot-to-paid conversion motion is documented.

## Phase 14 - GA Readiness

Goal: decide whether the product is ready for broad customer rollout.

Build:

- GA checklist.
- Release notes and upgrade guide.
- Support playbook.
- Customer admin docs.
- Final security, reliability, product, and GTM review.

Exit gate:

- No open P0/P1 findings.
- Production readiness checklist passes.
- At least one paid customer or signed expansion path exists.

## Phase 15 - Solo Showcase And Small-Team Rollout

Goal: produce a useful, claim-safe demo for a solo operator while corporate
design partners are unavailable.

Build:

- Lead-response operator showcase strategy in
  `docs/solo_showcase_plan.md`.
- Public AI policy and SOP source register.
- Lead-response operator role pack.
- Solo mini-cohort simulation.
- Training artifact report pack.
- UX demo gap decision.
- Readiness review for handoff to Lead Response SLA Agent.

Exit gate:

- Demo artifacts are source-linked and reproducible.
- Public/synthetic data is labeled as demo-only.
- No productivity, adoption, compliance, enterprise, or GA claim is made from
  public demo data.
- The next manual action is clear: show the artifact, improve it, or pause.

## Metrics That Matter

Product:

- Activation rate
- Assignment completion rate
- Guardrail pass rate
- Submission rate
- Manager review SLA
- Approved workflow changes per cohort
- Reused workflow changes after approval
- Risk flag rate

Quality:

- Retrieval hit@3, hit@5, MRR
- Citation precision
- No-answer accuracy
- Feedback faithfulness
- Human override rate
- Eval regression rate

Business:

- Pilot-to-paid conversion
- Time to launch first cohort
- Time to first approved workflow change
- Expansion from first team to second team
- Security review cycle time
- Gross retention of active teams

## Strategic Non-Goals Until PMF

- Broad LMS replacement.
- Generic prompt library marketplace.
- Fully autonomous policy approval.
- Productivity guarantees.
- SaaS-grade multi-tenant security claims without ADR and isolation tests.
- Deep integrations before a repeatable pilot workflow exists.
- Enterprise-facing rollout claims before solo/public-source demo artifacts are
  coherent and claim-safe.
