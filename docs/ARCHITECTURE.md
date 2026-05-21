# Architecture - AI Rollout Training OS

Version: 1.0
Last updated: 2026-05-19
Status: Draft

---

## System Overview

AI Rollout Training OS is a role-based AI adoption platform for training owners, learners, managers, and rollout operators. It turns company policies, SOPs, and role workflows into measurable missions, guardrail checks, AI-assisted rubric feedback, and manager-visible adoption evidence. The v1 system is a single-company deployment per pilot with a FastAPI application, PostgreSQL-backed state, text-only retrieval over policy/SOP documents, and bounded background jobs for feedback and reporting.

## Capability Profiles

| Profile | Status | Evaluation Artifact | Justification |
|---------|--------|---------------------|---------------|
| RAG | ON | `docs/retrieval_eval.md` | The product must ground feedback and guardrail checks in company AI policy, SOPs, role-pack content, allowed/forbidden use cases, and approved examples. These documents change during rollouts and must be cited in feedback, so prompt stuffing is not sufficient. Text-only retrieval is enough for v1 because users submit artifacts and source material as text. Implementation should adapt the proven Dream Motif Interpreter RAG/eval pattern documented in `docs/reference/dream_motif_rag_reuse.md`. |
| Tool-Use | OFF | n/a | v1 can call databases, retrieval, LLM providers, report exporters, and reminder services through deterministic application code. No LLM-directed external tool call or MCP-shaped integration is required in the initial design. Turning this on later requires an ADR and tool catalog. |
| Agentic | OFF | n/a | v1 does not require an observe-decide-act loop. Mission assignment, feedback jobs, and manager review are bounded workflows with deterministic state transitions. |
| Planning | OFF | n/a | The system may suggest follow-up missions, but its primary deliverable is training evidence and feedback, not a structured plan consumed by an execution engine. |
| Compliance | OFF | n/a | v1 must protect sensitive internal data and keep audit trails, but no named compliance framework or attestation is a launch gate. Formal compliance evidence collection requires an ADR. |

## Problem Fit and Adoption Reality

### Problem-First Entry Gate

| Question | Answer |
|----------|--------|
| Concrete operational pain | Teams are told to use AI but lack safe task boundaries, measurable practice, manager visibility, and evidence that use cases became repeatable workflow changes. |
| Current workaround | Ad hoc workshops, generic prompt libraries, Slack threads, one-off demos, unmanaged AI tool usage, and manual manager follow-up. |
| Why existing process is insufficient | Static training does not observe real task application. Prompt libraries do not teach verification, escalation, privacy handling, or workflow redesign. Manual feedback does not scale across cohorts or preserve evidence. |
| First user / operator who feels the pain | Operations leaders, enablement managers, AI transformation leads, and team managers running support, sales, operations, education, recruiting, or back-office pilots. |
| What would make v1 not worth adopting | Generic lessons with no role fit, no measurable work output, no manager dashboard, no guardrail testing, no company-policy alignment, or unauditable AI feedback. |
| First proof of value | At least 70 percent of enrolled users complete a role-specific mission, at least 50 percent submit a real workflow artifact, and managers approve at least 3 repeatable AI-assisted workflow changes from the pilot. |

### Adoption Reality Gate

| Boundary | Decision |
|----------|----------|
| Work AI is expected to improve | Drafting role-specific exercises, first-pass rubric feedback, use-case classification, evidence-grounded guardrail feedback, cohort risk summaries, and workflow-improvement suggestions. |
| Work AI will not replace | Manager judgment, HR policy ownership, legal/security approval, final certification, workflow accountability, and domain-expert review of submitted artifacts. |
| Claims not allowed before evidence | "Transforms the whole company", "replaces trainers", "guarantees productivity gains", "certifies safe AI use for regulated work", and "fully automates change management". |
| Demo-to-production evidence required | Completion, submission, guardrail pass, manager approval, human/AI rubric agreement, sensitive-data flag, retrieval quality, and p95 feedback-latency measurements from a pilot. |

## Solution Shape

| Decision | Selection | Justification |
|----------|-----------|---------------|
| Primary shape | Hybrid workflow | Deterministic workflow state, scoring, permissions, audit logs, and reporting are paired with bounded LLM calls for rubric feedback and synthesis. This is the minimum shape that addresses real-work feedback without granting the AI final authority. |
| Governance level | Standard | The project has medium blast radius, sensitive internal data risk, active RAG, and manager-facing adoption evidence. Lean governance is too light for auditability; Strict is not justified without regulated certification or high-risk destructive actions. |
| Runtime tier | T1 | The app needs a containerized web process, PostgreSQL with pgvector, and a bounded worker for LLM feedback jobs. No shell/package mutation, privileged runtime actions, or persistent autonomous worker state is needed. |

### Rejected Lower-Complexity Options

| Rejected option | Why it is insufficient |
|-----------------|------------------------|
| Deterministic-only | Rule-based scoring can track completion and quiz results, but it cannot provide useful first-pass feedback on real workflow artifacts against company-specific rubrics and policy evidence. |
| Static checklist or course | It would not collect submissions, compare outputs to rubrics, preserve policy snapshots, or show manager-visible adoption evidence. |
| Human-in-the-loop assistant only | A chat assistant would not create durable cohort state, audit trails, submission review states, or repeatable manager reports. |
| Simple tool use without workflow state | External calls alone do not solve mission assignment, feedback lifecycle, guardrail review, approvals, or longitudinal adoption metrics. |
| Higher-autonomy agent | The system does not need autonomous action selection or looped planning. Bounded jobs and deterministic state machines are safer and easier to evaluate. |

### Minimum Viable Control Surface

- Role-based access for operator, manager, and learner actions.
- Immutable audit events for authentication, submissions, feedback generation, approvals, exports, and policy snapshot changes.
- Text-only RAG with corpus versioning, citation traceability, and `insufficient_evidence` behavior.
- Deterministic scoring for completion, thresholds, routing, approval states, and report metrics.
- Human approval for certification, policy changes, approved examples, sensitive-data exceptions, and productivity claims.

### Human Approval Boundaries

| Boundary | Human approval required? | Why |
|----------|--------------------------|-----|
| Final certification or pass/fail status | Yes | AI feedback can inform review but cannot own accountability for training outcomes. |
| Company AI policy changes | Yes | Policy ownership remains with legal, security, HR, or management. |
| Publication of approved examples | Yes | Examples may contain proprietary process details or sensitive context. |
| Sensitive-data exception in a submitted artifact | Yes | Learners may paste customer or internal data; exceptions must be explicit. |
| Manager approval of workflow changes | Yes | Adoption proof requires manager judgment that the change is safe and useful. |
| Reminder sending and first-pass feedback | No | These are reversible or reviewable workflow actions when scoped to an enrolled cohort. |

### Deterministic vs LLM-Owned Subproblems

| Subproblem | Owner | Reason |
|------------|-------|--------|
| Authentication, authorization, and role checks | Deterministic | Access boundaries cannot depend on probabilistic output. |
| Required fields and mission completion state | Deterministic | Completion and eligibility must be reproducible. |
| Guardrail quiz scoring and pass thresholds | Deterministic | Learners and managers need stable outcomes. |
| Sensitive-data pattern detection | Deterministic first, LLM optional as advisory | Known categories should be caught by rules before any AI review. |
| Retrieval and citation selection | Hybrid | Retrieval is deterministic query/index logic; LLMs may summarize evidence but cannot fabricate citations. |
| Rubric feedback and workflow-improvement suggestions | LLM-owned with stored evidence | The value comes from nuanced feedback on text artifacts, but output must cite rubric and policy evidence. |
| Cohort metrics, adoption counts, and report totals | Deterministic | Reports must be auditable and comparable across cohorts. |
| Retries, idempotency, and audit triggers | Deterministic | Duplicate feedback or missing audit records would corrupt evidence. |

## Runtime and Isolation Model

| Property | Decision |
|----------|----------|
| Isolation boundary | T1 container boundary: web container, worker container, and PostgreSQL/pgvector service under Docker Compose for early pilots. |
| Persistence model | PostgreSQL stores users, cohorts, role packs, submissions, policy document metadata, chunks, feedback, approvals, jobs, and audit events. Object storage can be added later for files; v1 text artifacts stay in PostgreSQL. |
| Network model | Outbound egress only to the configured LLM provider and optional reminder/export services declared in environment configuration. No arbitrary runtime egress. |
| Secrets model | Secrets come from environment variables or deployment secrets. Source code, docs, tests, and logs never contain real API keys. |
| Runtime mutation boundary | Runtime cannot install packages, mutate toolchains, change services, or execute shell commands as product behavior. Deployments are rebuilt from source and migrations. |
| Rollback / recovery model | Roll back application containers to a previous image; database schema changes use Alembic migrations and backups; mission, rubric, policy, and report records are versioned. |

Lower runtime tiers are insufficient because the system needs a containerized database with pgvector and a bounded worker process. T2/T3 are not justified because no isolated mutable workspace, privileged action, or long-lived autonomous runtime is required.

## Inference / Model Strategy

| Path / Task | Model class | Deterministic alternative considered | Why this class | Fallback / escalation | Budget / latency constraint |
|-------------|-------------|--------------------------------------|----------------|-----------------------|-----------------------------|
| Use-case and risk classification | Small / fast structured-output model | Rule-only keyword categories | Rules miss role-specific nuance; a small model is enough because categories are bounded. | Fall back to deterministic risk labels and require manager review. | p95 under 10 seconds; low cost per submission. |
| Rubric feedback on submissions | Stronger reasoning model with structured output | Fixed rubric score only | The product value depends on specific feedback tied to the submitted artifact, rubric, and evidence. | If output validation fails twice, store `needs_human_review` and avoid scoring claims. | p95 under 60 seconds for normal text submissions. |
| Cohort risk summary | Mid-tier summarization model | Deterministic metric table only | Managers need concise synthesis of repeated risk patterns, not only counts. | Show deterministic dashboard metrics without narrative summary. | Batch/offline job; cost capped per cohort report. |
| Role-pack exercise drafting | Stronger model for operator-assist drafting | Hand-authored templates only | Drafting accelerates setup but remains human-approved before launch. | Operator can create or edit templates manually. | Operator path, not latency critical. |

## RAG Architecture

Implementation reference: adapt the RAG and eval implementation from `https://github.com/ashishki/Dream_Motif_Interpreter`, specifically the reusable surfaces mapped in `docs/reference/dream_motif_rag_reuse.md`. The reference is a starting point, not a vendor drop-in: dream-specific models, symbolic query expansion, and Telegram assistant behavior are out of scope.

### Ingestion Pipeline

`extract -> normalize -> chunk -> embed -> index`

| Stage | Description | Technology |
|-------|-------------|------------|
| Extract | Operator uploads or pastes company AI policy, SOPs, role descriptions, mission content, and approved examples as text/markdown. | FastAPI endpoints and PostgreSQL metadata records. |
| Normalize | Convert text/markdown to canonical plain text with source title, section path, document type, corpus version, and visibility scope. | Adapt Dream Motif `NormalizedDocument` / `SourceConnector` pattern with Pydantic validation. |
| Chunk | Split by headings first, then 512-token chunks with overlap. Preserve source section and policy snapshot ID. | Adapt Dream Motif `chunk_dream_text` pattern using `tiktoken`, renamed for policy/SOP chunks. |
| Embed | Create embeddings for normalized text chunks through an `EmbeddingClient` protocol. | Adapt Dream Motif embedding adapter shape; keep provider configured by environment. |
| Index | Store vectors and metadata in PostgreSQL using pgvector, with HNSW index once stable. | PostgreSQL 16 with pgvector; adapt Dream Motif vector migration and HNSW pattern. |

### Query-Time Pipeline

`query analyze -> retrieve -> filter -> assemble evidence -> answer | insufficient_evidence`

| Stage | Description | Technology |
|-------|-------------|------------|
| Query analyze | Build a retrieval query from mission, rubric, learner answer, and policy question. | Deterministic query builder plus optional small-model rewrite after evaluation. |
| Retrieve | Similarity search within the active company corpus and policy snapshot. | Adapt Dream Motif hybrid pgvector cosine + PostgreSQL FTS retrieval with reciprocal rank fusion. |
| Filter | Enforce document type, role pack, cohort, and active policy version filters. | SQL filters and score thresholds. |
| Assemble evidence | Format chunks as cited evidence blocks with source IDs and snippets. | Adapt Dream Motif `EvidenceBlock` / `InsufficientEvidence` shape, replacing dream fragments with source citation fields. |
| Answer / insufficient_evidence | Feedback generation may answer only when evidence meets coverage threshold; otherwise returns `insufficient_evidence`. | Structured LLM output validator. |

The `insufficient_evidence` path is mandatory. When evidence is missing, stale, or below threshold, the system must return `insufficient_evidence` and route the submission to human review instead of inventing policy guidance.

### Corpus Description

| Property | Value |
|----------|-------|
| Source documents | Company AI policy, allowed/forbidden use cases, role-specific SOPs, mission rubrics, training content, and approved example submissions. |
| Update frequency | Monthly or faster during a rollout. Updates create a new corpus version or policy snapshot. |
| Estimated size | v1 pilot: tens to hundreds of documents, hundreds to low thousands of chunks. |
| Access control | v1 assumes one company workspace per deployment. All retrieval queries are scoped to the active workspace and policy snapshot. Future multi-tenant SaaS requires ADR and stronger tenant isolation. |

### Retrieval / Embedding Strategy

| Decision | Selection | Why |
|----------|-----------|-----|
| Retrieval mode | text-only | v1 inputs are text artifacts, pasted SOPs, markdown policies, and textual rubrics. Multimodal evidence can wait until screenshots, Looms, slides, or spreadsheets become required pilot data. |
| Modalities in scope | text only | Text provides enough signal for feedback, guardrail checks, and reports in v1. |
| Text-only baseline considered? | yes | Text-only is the baseline and must be evaluated before any multimodal expansion. |
| Embedding provider / model | Stable text embedding model configured by env | Keeps provider choice swappable while preserving index schema versioning. |
| Stability status | stable | Preview embedding models are not allowed for manager-facing feedback without ADR and re-index plan. |
| Fallback / migration path | Keep source chunks and corpus version metadata so embeddings can be rebuilt if provider/model changes. | Retrieval remains recoverable after model migration. |

### Index Strategy

- Embedding model: configured by `EMBEDDING_MODEL`, default stable text embedding model.
- Chunking: section-aware chunks around 512 tokens with roughly 50-token overlap; preserve heading path, source document ID, snapshot ID, and workspace ID.
- Vector representation contract: fixed by `index_schema_version = v1`; vector dimensions must match the configured embedding model and require ADR if changed.
- Index schema version: v1; changes require ADR and full re-index.
- Max index age: 7 days for active pilot corpora.
- Evaluation plan: adapt Dream Motif `scripts/eval.py` pattern to seed a synthetic policy/SOP corpus, compute hit@3, hit@5, MRR, citation precision, no-answer accuracy, and latency, and write valid Eval Source / Date / Corpus Version rows into `docs/retrieval_eval.md`.

### Risks (RAG-specific)

| Risk | Mitigation |
|------|------------|
| Hallucination on weak evidence | Required score/coverage threshold and `insufficient_evidence` path. |
| Schema drift | Version chunking, metadata, and embedding model under index schema v1; ADR and full re-index on change. |
| Stale index | Health endpoint exposes active corpus version and index age; stale corpora beyond 7 days produce warning or non-ready status. |
| Corpus isolation failure | Workspace and policy snapshot filters are enforced in retrieval SQL before evidence assembly. |
| Retrieval latency regression | Retrieval p95 tracked in `docs/retrieval_eval.md` and CI eval tests after automation exists. |
| Multimodal complexity creep | Multimodal is out of scope until an ADR shows text-only is insufficient on pilot evidence. |

## Component Table

| Component | File / Directory | Responsibility |
|-----------|------------------|----------------|
| API application | `ai_rollout_os/main.py` | FastAPI app factory, middleware wiring, health endpoint. |
| Configuration | `ai_rollout_os/core/config.py` | Environment parsing, fail-fast validation, model/provider settings. |
| Observability | `ai_rollout_os/observability/` | Structured logging, tracing helper, metrics hooks, PII-safe instrumentation. |
| Auth and roles | `ai_rollout_os/auth/` | Operator, manager, and learner authentication and authorization checks. |
| Database models | `ai_rollout_os/db/` | SQLAlchemy models, sessions, repositories, migrations. |
| Role packs and missions | `ai_rollout_os/training/` | Role-pack definitions, mission templates, guardrail quizzes, cohort assignment. |
| Submissions | `ai_rollout_os/submissions/` | Learner artifact submission, review state, redaction status, storage. |
| Retrieval | `ai_rollout_os/retrieval/` | Document normalization, chunking, embedding, pgvector indexing, query-time evidence assembly. |
| Retrieval evaluation | `scripts/eval.py`, `tests/eval/` | Synthetic policy/SOP corpus seeding, retrieval metrics, no-answer checks, and eval-history updates adapted from Dream Motif Interpreter. |
| Feedback | `ai_rollout_os/feedback/` | Rubric evaluation, structured LLM output validation, feedback persistence. |
| Reporting | `ai_rollout_os/reporting/` | Manager dashboard metrics, progress exports, cohort summaries. |
| Background jobs | `ai_rollout_os/jobs/` | Postgres-backed feedback and reminder job execution. |
| Audit | `ai_rollout_os/audit/` | Append-only audit event writes and query helpers. |

## Data Flow

### Learner Submission And Feedback

1. Learner submits `POST /missions/{mission_id}/submissions` with session auth and a text artifact.
2. Middleware authenticates the learner and verifies cohort/mission eligibility.
3. Submission service validates required fields, stores the artifact, records the policy snapshot ID, and emits an audit event.
4. Redaction service checks known sensitive-data patterns and marks the submission `blocked_for_review` or `ready_for_feedback`.
5. Feedback job retrieves the active mission rubric and policy/SOP evidence through the RAG query service.
6. If evidence is insufficient, the job stores `needs_human_review` with cited missing evidence reason.
7. If evidence is sufficient, the LLM feedback service produces structured rubric feedback with citations and validation.
8. Manager dashboard reads stored feedback, completion status, guardrail result, and approval state from PostgreSQL.

### Operator Policy Update

1. Operator submits policy/SOP text through an authenticated admin route.
2. Document registry creates a new policy snapshot and document version.
3. Ingestion job normalizes, chunks, embeds, and indexes the document under index schema v1.
4. Health endpoint exposes corpus freshness and active index version.

## Tech Stack

| Component | Choice | Rationale |
|-----------|--------|-----------|
| Language | Python 3.12 | Fits FastAPI, Pydantic, LLM integrations, and existing stack preference. |
| API framework | FastAPI | Strong typed request/response contracts and simple async routes. |
| Validation | Pydantic v2 | Required for structured LLM outputs, config parsing, and API schemas. |
| Database | PostgreSQL 16 + pgvector | Stores transactional training records and vector index in one operational surface for v1. This matches the proven Dream Motif Interpreter retrieval stack. |
| ORM / migrations | SQLAlchemy 2.x + Alembic | Explicit transactions, migrations, and testable repository boundaries. |
| Background jobs | PostgreSQL-backed job table with worker process | Avoids Redis dependency in v1 while supporting retryable feedback jobs and reminders. |
| LLM provider | Provider adapter behind `ai_rollout_os/ai/` | Keeps model choices per workload and prevents provider coupling in business services. |
| Observability | Structured stdlib logging plus shared tracing adapter | Enough for early pilots; can map to OpenTelemetry later through one module. |
| Lint / format | ruff | Single tool for lint and format checks. |
| Test framework | pytest | Supports unit, integration, and eval tests. |
| CI | GitHub Actions | Native to repo, enough for lint, format, database-backed tests, and retrieval eval gates. |
| Deployment | Docker Compose on VPS | Matches early pilot target and T1 runtime boundary. |

## Security Boundaries

### Authentication

`GET /health` is public. All other routes require session or bearer-token authentication issued by the app. v1 supports operator/admin, manager, and learner roles. Tokens expire and are validated server-side; future Google Workspace or SSO integration requires ADR.

### Workspace Boundary

v1 assumes one company workspace per deployment. The system still stores `workspace_id` on workspace-scoped records so future multi-tenant support has an explicit migration path, but it does not claim SaaS-grade tenant isolation until an ADR introduces RLS or separate database strategy.

### PII And Sensitive Data Policy

No PII or proprietary workflow text may appear in logs, span attributes, metrics labels, or client error messages. Sensitive fields include user email, full name, learner submission text, manager comments, company policy text, SOP text, customer names embedded in submissions, and proprietary process descriptions. Observability may include hashed IDs, counts, status enums, and trace IDs.

## Observability

| Dimension | Choice | Notes |
|-----------|--------|-------|
| Tracing | Shared tracing adapter | Module: `ai_rollout_os/observability/tracing.py`. |
| Metrics | In-process counters first, Prometheus-compatible export later | Required labels: `service`, `env`, `operation`; no user text or names. |
| Logging | Structured JSON logs through stdlib | Required fields: `trace_id`, `env`, `service`, `operation`, `result`. |
| Dashboards | Manager dashboard for product metrics; ops dashboard TBD | Pilot metrics must come from stored deterministic records. |
| Alerting | TBD by deployment | At minimum, feedback job failures and stale index warnings are visible in health/readiness. |

### Observability Invariants

- No PII or proprietary text in spans, metrics labels, logs, or returned errors.
- `GET /health` returns health plus index freshness without leaking document contents.
- DB, LLM, embedding, report export, and reminder calls are instrumented through shared modules.

## External Integrations

| Integration | Purpose | Auth method | Rate limit / SLA |
|-------------|---------|-------------|------------------|
| LLM provider API | Classification, feedback, synthesis, role-pack drafting, embeddings. | API key from environment. | Provider-specific; app enforces retry and timeout budgets. |
| Google Drive/Docs or Notion | Optional policy/SOP import after manual upload path exists. | OAuth or service token, future ADR before production. | Integration-specific; out of initial critical path. |
| Slack or Teams | Optional reminders and manager alerts after deterministic reminder scheduler exists. | Webhook URL from environment. | Provider-specific; retries idempotent by reminder ID. |
| CSV/Markdown export | Exportable progress report. | No external credential required. | Local generation. |

## File Layout

```text
AI-Rollout-Training-OS/
├── ai_rollout_os/
│   ├── __init__.py
│   ├── main.py
│   ├── ai/
│   ├── audit/
│   ├── auth/
│   ├── core/
│   ├── db/
│   ├── feedback/
│   ├── jobs/
│   ├── observability/
│   ├── reporting/
│   ├── retrieval/
│   ├── submissions/
│   └── training/
├── migrations/
├── tests/
│   ├── unit/
│   ├── integration/
│   └── eval/
├── docs/
│   ├── ARCHITECTURE.md
│   ├── CODEX_PROMPT.md
│   ├── DECISION_LOG.md
│   ├── EVIDENCE_INDEX.md
│   ├── IMPLEMENTATION_CONTRACT.md
│   ├── IMPLEMENTATION_JOURNAL.md
│   ├── retrieval_eval.md
│   ├── spec.md
│   ├── tasks.md
│   ├── adr/
│   ├── audit/
│   └── prompts/
├── .github/workflows/ci.yml
├── requirements.txt
├── requirements-dev.txt
├── pyproject.toml
└── README.md
```

## Runtime Contract

| Variable | Description | Example value | Required |
|----------|-------------|---------------|----------|
| `APP_ENV` | Runtime environment name. | `test` | Yes |
| `DATABASE_URL` | PostgreSQL connection URL. | `postgresql+psycopg://user:pass@localhost:5432/ai_rollout` | Yes |
| `SECRET_KEY` | Signing key for sessions or bearer tokens. | `change-me-in-env` | Yes |
| `AI_PROVIDER_API_KEY` | API key for the configured LLM provider. | `test-key` | Yes outside pure unit tests |
| `MODEL_FAST` | Model ID for classification and bounded checks. | `fast-structured-model` | Yes |
| `MODEL_STRONG` | Model ID for feedback and synthesis. | `reasoning-feedback-model` | Yes |
| `EMBEDDING_MODEL` | Stable text embedding model ID. | `stable-text-embedding-model` | Yes |
| `INDEX_MAX_AGE_DAYS` | Maximum acceptable active corpus age. | `7` | No, default `7` |
| `FEEDBACK_TIMEOUT_SECONDS` | Per-feedback job timeout. | `60` | No, default `60` |
| `RETENTION_DAYS` | Artifact retention period before deletion/redaction workflow. | `365` | No, default `365` |

## Continuity and Retrieval Model

### Canonical Truth

| Artifact | Authority |
|----------|-----------|
| `docs/ARCHITECTURE.md` | Architecture, runtime, profile, and boundary decisions. |
| `docs/IMPLEMENTATION_CONTRACT.md` | Immutable implementation rules. |
| `docs/spec.md` | Product behavior and acceptance scope. |
| `docs/tasks.md` | Task graph and implementation contract per task. |
| `docs/CODEX_PROMPT.md` | Live session state, baseline, findings, and next task. |
| `docs/adr/` | Approved architecture changes. |
| `docs/audit/` and `docs/retrieval_eval.md` | Review and profile-specific evidence. |

### Retrieval Convenience

| Artifact | Purpose | Required? |
|----------|---------|-----------|
| `docs/DECISION_LOG.md` | Quick index of major decisions and canonical sources. | Yes |
| `docs/IMPLEMENTATION_JOURNAL.md` | Cross-session handoff and durable implementation notes. | Yes |
| `docs/EVIDENCE_INDEX.md` | Index of tests, evals, audits, and proof artifacts. | Yes, because RAG eval and audit evidence are active. |

### Scoped Retrieval Rules

- Tasks touching architecture, runtime, auth, retrieval semantics, sensitive data, migrations, or open findings must include `Context-Refs`.
- Agents read scoped references before broad searching.
- Retrieval artifacts summarize and index. They do not overrule canonical files.

## Non-Goals

- No full LMS replacement in v1.
- No regulated certification or proctored exams in v1.
- No public course marketplace or community features in v1.
- No autonomous rewriting of company policy.
- No broad SaaS multi-tenancy claim until an ADR defines tenant isolation and test strategy.
- No multimodal retrieval until text-only retrieval fails a documented pilot need.
- No T2/T3 runtime, shell mutation, or autonomous agent loop without ADR.
