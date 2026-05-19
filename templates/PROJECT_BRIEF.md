# Project Brief: AI Rollout Training OS

Use this document before running `prompts/STRATEGIST.md`. The goal is not to pre-design the system, but to give the Strategist enough context to choose the right solution shape, governance level, runtime tier, and model strategy without guessing.

---

## 1. Project

- **Project name:** AI Rollout Training OS
- **One-sentence summary:** A role-based AI adoption platform that turns company workflows into measurable training missions, guardrail checks, and adoption evidence for non-technical teams.
- **Why this project exists:** Many teams already have access to AI tools, but adoption fails because employees do not know which tasks are appropriate, how to verify outputs, what is forbidden, or how to turn experiments into repeatable workflow changes. The market does not need another inspirational AI course; it needs a practical rollout system with assignments, eval rubrics, policy boundaries, and adoption metrics.
- **What success looks like in v1:** One team completes a role-specific training track, submits real workflow exercises, receives AI-assisted feedback, passes guardrail checks, and produces measurable adoption evidence such as saved time, approved use cases, reusable prompts/SOPs, and manager-visible progress.

## 1b. Problem Fit and Adoption Reality

Answer these before describing the desired architecture. The Strategist uses
this section to avoid designing a polished AI system around an unproven or
demo-only need.

- **Concrete operational pain:** Teams are told to "use AI" but lack a safe operating model. Employees experiment inconsistently, managers cannot see which use cases are valuable, and legal/security concerns block adoption because nobody has explicit boundaries or proof of responsible usage.
- **Current workaround:** Ad hoc workshops, generic prompt libraries, internal Slack threads, one-off demos, unmanaged ChatGPT usage, and manual manager follow-up.
- **Why existing process is insufficient:** Static training does not observe whether people can apply AI to real tasks. Prompt libraries do not teach verification, escalation, privacy handling, or workflow redesign. Manual training does not scale feedback or maintain evidence across teams.
- **First user / buyer / operator who feels the pain:** Operations leaders, enablement/training managers, AI transformation leads, and team managers in support, sales, operations, education, recruiting, or back-office teams.
- **What would make v1 not worth adopting:** Generic lessons with no role fit, no measurable work output, no manager dashboard, no guardrail testing, no company-policy alignment, or AI feedback that cannot be audited.
- **Adoption proof metric:** At least 70 percent of enrolled users complete a role-specific mission, at least 50 percent submit a real workflow artifact, and managers approve at least 3 repeatable AI-assisted workflow changes from the pilot.
- **Claims that are out of bounds before evidence:** "Transforms the whole company", "replaces trainers", "guarantees productivity gains", "certifies safe AI use for regulated work", "fully automates change management".
- **Work AI will not replace:** Manager judgment, HR policy ownership, legal/security approval, final certification, workflow accountability, and domain-expert review of submitted artifacts.

## 2. Users and Workflows

- **Primary users / operators:** Team members learning AI-assisted workflows, team managers reviewing adoption, enablement/training owners configuring tracks, and AI rollout operators maintaining content and rubrics.
- **Main workflow 1:** Training owner selects a role pack, imports company policy/SOP context, configures allowed tools and forbidden use cases, and launches a cohort.
- **Main workflow 2:** Learners complete short missions using their real work context, submit outputs, answer guardrail questions, and receive structured feedback.
- **Main workflow 3:** Managers review progress, approved workflow changes, flagged risks, reusable examples, and adoption metrics; the operator updates missions and rubrics based on real failures.

## 3. Scope

- **In scope for v1:** One or two role packs, mission templates, assignment submission, AI-assisted feedback, deterministic completion scoring, guardrail quizzes, manager dashboard, exportable progress report, and a small company-policy knowledge base.
- **Out of scope / non-goals:** Full LMS replacement, enterprise HRIS integration, regulated certification, proctored exams, broad marketplace of courses, public community features, and autonomous rewriting of company policy.

## 4. AI Scope

- **Where AI may be needed:** Turning SOPs into role-specific exercises, reviewing submitted artifacts against rubrics, giving feedback, classifying use cases, suggesting workflow improvements, summarizing cohort risks, and adapting examples to company context.
- **Where AI is explicitly not wanted:** Final pass/fail certification, policy approval, HR records, access control, score calculations, completion tracking, identity management, and audit log writes.
- **Possible retrieval / RAG need:** Yes. The system needs retrieval over company policy, allowed/forbidden AI use cases, role-specific SOPs, examples of approved submissions, and training materials.
- **If retrieval is needed, is text-only likely sufficient or is multimodal evidence truly required:** Text-only is sufficient for v1. Users can paste work artifacts, SOPs, and answers as text.
- **If multimodal may be needed, which modalities and why:** Later versions may accept screenshots, Loom walkthroughs, slide decks, or spreadsheet examples to review real workflows more naturally.
- **Possible tool-use need:** Yes. Tools may read knowledge-base documents, grade submissions against rubrics, generate feedback, export reports, send reminders, and create follow-up tasks.
- **Possible planning / agentic behavior need:** Limited. The system can suggest next missions based on progress, but it should not independently certify users or change policy.

## 5. Deterministic Candidates

List the parts that probably should stay deterministic unless the Strategist proves otherwise.

- **Validation / policy checks:** Required fields, forbidden data categories, role/track eligibility, mission completion status, allowed tool list, and mandatory approval checkpoints.
- **Routing / decision rules:** Which submissions need manager review, which risks trigger escalation, which mission comes next, and which cohort metrics appear in reports.
- **Calculations / transformations:** Completion rate, pass/fail thresholds, time-to-completion, adoption counts, manager approval counts, and rubric score aggregation.
- **Retries / idempotency / audit triggers:** Submission IDs, feedback generation retries, immutable audit events, report versioning, and policy-context snapshot IDs.

## 6. Human Approval Boundaries

- **What actions must require human approval:** Certification, policy changes, publication of approved examples, use of sensitive data in exercises, manager approval of workflow changes, and any claim about productivity gains.
- **What can be automated safely:** Mission assignment, reminder sending, first-pass rubric feedback, risk flagging, progress reporting, and suggestion of follow-up practice.
- **Why these boundaries matter:** AI adoption is a change-management and trust problem. The system must make teams safer and more measurable, not create a black-box training authority.

## 7. Risk and Error Cost

- **What is expensive if the system is wrong:** Employees may learn unsafe practices, share sensitive data, overtrust AI outputs, or managers may believe adoption is stronger than it is.
- **What is expensive if the system is slow:** Cohort momentum drops, reminders become stale, and rollout loses executive attention. Real-time latency is less critical than reliable feedback loops.
- **What is expensive if the system is inconsistent / variable:** Learners receive conflicting guidance, managers lose trust in scores, and training outcomes cannot be compared across cohorts.
- **Blast radius if it fails badly:** Medium. It can create risky AI usage norms across a team. In regulated environments the blast radius could be high, so v1 should avoid regulated certification claims.
- **Audit / explainability needs:** High. Managers must see why feedback was given, which policy/rubric applied, and which submissions triggered risks.

## 8. Data

- **Primary data sources:** Role descriptions, SOPs, company AI policy, training content, learner submissions, manager feedback, guardrail quiz answers, approved examples, and progress events.
- **Approximate data volume:** v1 pilot may include 20-100 learners, 5-20 missions, and hundreds of submitted text artifacts.
- **Does data change frequently:** Yes. Policies, tools, role workflows, and approved use cases may evolve monthly or faster during rollout.
- **Sensitive / regulated data present:** Potentially yes. Learners may paste customer data, internal documents, or proprietary workflows. v1 should include explicit data handling guidance and redaction checks.
- **Retention / deletion expectations:** Retain training records, feedback, and audit metadata; allow deletion/redaction of submitted artifacts when they include sensitive content.

## 8b. Continuity and Evidence

- **Which decisions are likely to be revisited later:** Role-pack design, rubric revisions, policy boundary changes, approved use cases, failed submissions, and manager adoption decisions.
- **What prior evidence or proof will future agents need to find quickly:** Training mission versions, user submissions, feedback, policy snapshots, manager approvals, cohort metrics, and examples that became reusable SOPs.
- **Will work span multiple sessions / agents / weeks:** Yes. Rollouts happen over weeks and require iteration across cohorts.
- **Any existing docs, ADRs, audits, or notes that should become retrieval anchors:** The operator's AI workflow playbook, eval/guardrail patterns from `gdev-agent`, evidence-memory patterns from `telegram-research-agent`, and prior education/training experience from B2B programs.

## 9. Integrations

- **External APIs / services:** Google Drive/Docs, Notion, Slack or Telegram reminders, Airtable/Sheets exports, optional LMS links, and LLM provider APIs.
- **Databases / storage:** PostgreSQL for structured training records; object/file storage for uploaded policy/SOP files if needed; vector index for policy and example retrieval.
- **Auth / identity provider:** Simple operator/admin login for v1; later Google Workspace or SSO if used inside companies.
- **Webhooks / messaging / queues:** Reminder jobs, assignment notifications, manager-review alerts, and optional Slack/Telegram command interface.

## 10. Constraints

- **Preferred stack:** Python, FastAPI, PostgreSQL, Redis or simple background jobs, Pydantic structured outputs, Markdown/HTML reports, and a minimal web UI or admin CLI for v1.
- **Deployment target:** VPS or Docker Compose for early pilots. Managed deployment can come later if there is a repeatable sales motion.
- **Budget constraints:** Medium. The system should use smaller models for grading/routing and stronger models only for nuanced feedback or cohort synthesis.
- **Latency / throughput expectations:** Feedback should return in under 30-60 seconds for normal submissions. Manager dashboards should load immediately from stored results.
- **Compliance requirements:** No formal compliance certification in v1. Treat internal company data carefully and maintain audit trails.
- **Network / security restrictions:** Store credentials in environment/secrets, restrict access by cohort/admin role, redact sensitive submissions from logs.

## 11. Runtime and Operations

- **Should runtime stay simple (managed service / container) if possible:** Yes. Start as a small web app or CLI-backed pilot with scheduled reminders and stored reports.
- **Any need for shell, package, or toolchain mutation at runtime:** No.
- **Any need for privileged actions or long-lived isolated workers:** No privileged actions. Background workers may be useful for feedback generation and reminders.
- **Recovery / rollback expectations:** Mission, rubric, and policy versions must be recoverable. Failed feedback jobs should be retryable without duplicating submissions.

## 12. Model and Cost Expectations

Only fill what you know. The Strategist should still make the final recommendation.

- **Cost sensitivity:** medium
- **Latency sensitivity:** medium
- **Expected request / task volume:** Pilot volume is hundreds of feedback/evaluation calls per cohort, plus occasional synthesis reports.
- **If AI is used, should the system prefer smaller / cheaper models by default:** Yes. Use cheaper models for classification and rubric checks; reserve stronger models for high-quality feedback and cohort-level synthesis.
- **Any required capabilities:** Structured output, retrieval-grounded feedback, rubric evaluation, summarization, role adaptation, and moderate reasoning.
- **Preview-model tolerance:** low for scoring/feedback used in manager reports; medium for internal content drafting.

## 13. Success Metrics

- **Business success metric:** Number of teams completing a pilot and converting to a paid rollout or consulting engagement.
- **Quality metric:** Manager-approved percentage of AI-assisted workflow artifacts and agreement rate between human review and AI rubric feedback.
- **Latency metric:** p95 feedback generation under 60 seconds.
- **Cost metric:** LLM cost per learner and per completed mission stays within a configured budget.
- **Operational metric:** Cohort completion rate, guardrail pass rate, number of approved reusable workflows, manager review backlog, and sensitive-data flag rate.

---

## Usage

1. Send this completed brief to the Strategist.
2. Let the Strategist ask one batch of clarifying questions.
3. Use the resulting architecture package as the Phase 1 input to the rest of the playbook.
