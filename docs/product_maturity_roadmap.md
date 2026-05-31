# Product Maturity Roadmap

Version: 1.0
Date: 2026-05-19
Status: post-MVP planning artifact

This roadmap turns the current pilot-ready MVP into a mature production product.
It is written for the Codex-only AI loop and pairs with
`docs/product_maturity_task_graph.md`.

---

## Strategic Thesis

The active v1 product direction is the **Agent Permission Training Simulator**.
The product should not mature into a generic LMS or broad prompt-training
library. The sharper market wedge is permission judgment for teams adopting AI
agents:

> Teach teams when to approve, deny, clarify, sandbox, or escalate agent
> requests before those habits become unsafe operational defaults.

The buyer pain is not "employees need prompt training." The urgent pain is that
teams are being asked to approve agent actions around files, commands, secrets,
dependencies, CI, logs, and network calls without a shared decision model.

## Target Market Wedge

- ICP: engineering, support, enablement, or operations teams adopting Cursor,
  Codex, Claude Code, or similar AI agent tools.
- Initial buyer: AI Transformation lead, Engineering Enablement, Security,
  Developer Productivity, Support Enablement, or team lead responsible for safe
  AI rollout.
- Internal blockers: Security, Legal, Compliance, IT, Procurement, and managers
  worried about unsafe approvals.
- First use case: a fast workshop/demo that teaches permission decisions before
  broad platform rollout.

Avoid broad horizontal positioning until the simulator proves repeated
willingness to pay as a focused workshop/demo pack.

## Maturity Principles

- Prove value before expanding surface area.
- Make the permission simulator useful before adding LMS or enterprise platform
  workflows.
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
| 16 | Visual Permission Simulator | Can the product teach agent permission judgment through a polished, monetizable simulator? | Scenario library, scoring, visual prototype, and workshop pack are ready. |
| 17 | Ship It? Y/N Product And Architecture Blueprint | Can the mini-game be specified as the next polished public product surface without shrinking the idea? | Product spec, scenario schema, React/Vite architecture, visual direction, and task graph are aligned. |
| 18 | Scenario And Scoring Core | Can the full seven-level game be driven by validated data and deterministic scoring? | Seven scenarios, Pydantic validation, meter deltas, badges, and safety guards pass tests. |
| 19 | React/Vite Playable Game | Can the game feel beautiful, convenient, and playable in one browser session? | React/Vite public game runs through all seven levels with terminal UI, inspect/diff, meters, badges, and final report. |
| 20 | Browser Polish And Public Demo Evidence | Can the public game be shown without caveats? | Browser e2e, desktop/mobile screenshots, README visual artifact, and UX readiness review pass. |
| 21 | Workshop, Analytics, And Buyer Validation | Can the game become a workshop wedge and evidence loop? | Facilitator pack, safe aggregate summary, analytics-lite, buyer feedback loop, and claim-boundary review are ready. |

## Phase 16 - Visual Permission Simulator Pivot

The next product direction and active v1 is an Agent Permission Training
Simulator. The product should teach teams how to evaluate agent requests such as
reading secrets, editing command surfaces, running tests after script changes,
installing dependencies, deleting files, editing CI workflows, making network
calls, or following instructions embedded in test output and logs.

The v1 user action set is:

- approve
- deny
- ask for clarification
- run in sandbox
- escalate to reviewer

The simulator should prioritize visual clarity, scenario quality, scoring, and
lesson text over enterprise LMS features. It remains grounded in the existing
governance/evidence model, but the first monetizable artifact is a demo/workshop
experience.

The v1 teaching taxonomy is:

- allowed: action is low-risk and inside the approved scope.
- needs approval: action may be valid but requires reviewer, manager, security,
  or policy-owner approval.
- blocked: action should be denied because it exposes secrets, destroys
  evidence, exceeds scope, or crosses a forbidden boundary.
- unknown: action needs clarification because the request lacks enough context
  for a safe decision.

## Next Pivot: Ship It? Y/N

Phase 17 starts the next AI-assisted development cycle. The goal is not to
compress the simulator into a small quiz. The goal is a polished
React/Vite-powered public mini-game that makes agent permission risk feel real
through pressure, tradeoffs, consequence feedback, meters, and a shareable final
report.

Ship It? Y/N is the front door for the Agent Permission Training Simulator:

- a 3 to 7 minute public game;
- seven memorable scripted levels;
- terminal-style developer UI;
- inspect/diff, sandbox, scope, eval, escalation, and rollback mechanics;
- deterministic scoring;
- browser-level evidence;
- workshop integration after the playable demo is polished.

Frontend decision:

- build the game as React + Vite + TypeScript + Tailwind under
  `frontend/permission_game/`;
- serve the built bundle from FastAPI at `/demo/ship-it-yn`;
- keep public game persistence local-only until a later authenticated workshop
  surface exists.

Do not build a real agent runner. Do not execute commands, read local files,
request real credentials, or use live LLM scoring.

## Phase 17 - Ship It? Y/N Product And Architecture Blueprint

Goal: define the complete product, scenario, visual, and technical blueprint
before implementation.

Build:

- product spec;
- scenario schema;
- React/Vite frontend architecture;
- visual and copy direction;
- AI development plan;
- task graph and state alignment.

Exit gate:

- `docs/ship_it_yn_product_spec.md`,
  `docs/permission_game_scenario_schema.md`,
  `docs/ship_it_yn_frontend_architecture.md`, and
  `docs/ship_it_yn_ai_development_plan.md` agree on the game shape.
- Active next task is T75.
- React/Vite is explicitly selected for the polished game UI.

## Phase 18 - Scenario And Scoring Core

Goal: make the game data-driven and deterministic.

Build:

- seven starter scenarios;
- Pydantic validation;
- scoring outcomes for correct, partial, unsafe, and overblock choices;
- meter deltas for velocity, blast radius, trust, eval confidence, and audit
  trail;
- badge/title logic;
- local session model;
- safety guards against real execution, real secrets, and unsafe claims.

Exit gate:

- all seven scenarios validate;
- every playable choice has feedback;
- scoring and badges are tested;
- no live LLM or real command execution path exists.

## Phase 19 - React/Vite Playable Game

Goal: build the beautiful public game, not just a form.

Build:

- React/Vite/TypeScript/Tailwind scaffold;
- terminal layout;
- scenario card;
- decision buttons and keyboard shortcuts;
- inspect/diff drawer;
- risk meters;
- audit trail;
- consequence panel;
- badge notifications;
- final report and share text.

Exit gate:

- one full seven-level run works locally;
- desktop and mobile layouts are stable;
- UI is polished enough to show without explaining unfinished controls.

## Phase 20 - Browser Polish And Public Demo Evidence

Goal: make `/demo/ship-it-yn` demo-ready with real browser proof.

Build:

- FastAPI static serving for the Vite bundle;
- browser e2e for the public game path;
- desktop and mobile screenshots;
- README GIF or screenshot;
- accessibility pass;
- UX readiness review.

Exit gate:

- browser automation passes;
- screenshots are nonblank and correctly framed;
- README points to the game and visual artifact;
- P2-UX-001 is narrowed or closed for the public game scope.

## Phase 21 - Workshop, Analytics, And Buyer Validation

Goal: turn the game into a credible workshop and buyer-learning wedge.

Build:

- facilitator debrief;
- team summary report;
- safe local/session analytics;
- buyer feedback template;
- scenario authoring workflow;
- claim boundary and security review;
- readiness review for manual buyer demos.

Exit gate:

- the game can start a team discussion about risk hotspots;
- aggregate reporting avoids personal shame mechanics;
- no unsupported claims are made about compliance, production readiness, PMF, or
  paid conversion.

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
