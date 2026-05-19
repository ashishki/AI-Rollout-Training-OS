# Implementation Contract - AI Rollout Training OS

Status: IMMUTABLE - changes require an ADR filed in `docs/adr/`
Version: 1.0
Effective date: 2026-05-19

Any finding that this contract was violated is automatically P1 unless a stricter severity is stated.

---

## Universal Rules

### SQL Safety

- All SQL is parameterized. Use SQLAlchemy expressions or `text()` with named parameters.
- Never interpolate variables into SQL strings. This includes f-strings, `%` formatting, `.format()`, and string concatenation.
- Never use string concatenation to build table names, column names, filters, or `ORDER BY` clauses.
- Violation: automatic P1.

### Authorization

- Every route except `GET /health` enforces authentication and authorization before accessing data.
- Authorization means the caller identity is verified and the caller role is allowed to perform the action.
- Operator, manager, and learner permissions are checked at the route/service boundary before database mutation.
- If a route is intentionally public, it must include a code comment citing the design decision.
- Violation: automatic P1.

### PII Policy

- No PII, learner submission text, company policy text, SOP body text, manager notes, or proprietary workflow text in log messages.
- No PII or proprietary text in span attributes.
- No PII or proprietary text in metrics labels or metric values.
- No PII or proprietary text in client error messages.
- Where identifiers must appear in observability data, use opaque IDs or SHA-256 hashes.
- Fields considered sensitive in this project: email, full name, learner submission text, manager comments, company policy text, SOP text, customer names embedded in submissions, proprietary process descriptions, API keys, tokens, and passwords.
- Violation: automatic P1.

### Credentials And Secrets

- No credentials, API keys, tokens, passwords, or secrets in source code.
- No credentials in comments, docs examples, or test fixtures. Tests use placeholder values such as `test-key`.
- All real secrets come from environment variables or deployment secrets.
- `.env` files are ignored and are never committed.
- Violation: automatic P1 and security incident.

### Shared Tracing Module

- One shared tracing module: `ai_rollout_os/observability/tracing.py`.
- All code that creates spans imports from this module.
- No inline noop span implementations in individual files.
- No copy-pasted tracer initialization in individual modules.
- Violation: P2; escalates to P1 at age cap.

### CI Gate

- CI must pass before merge.
- A PR with failing CI is never merged.
- CI flakiness is fixed before merge, not bypassed.
- Phase 1 includes CI setup and first test baseline.
- Violation: automatic P1.

### Observability

- Every external call to PostgreSQL, LLM provider, embedding provider, HTTP API, or reminder delivery adapter is wrapped in a span with `trace_id` and operation name.
- For each external-call type, emit success/error counters and latency measurements once the metrics module exists.
- `GET /health` returns HTTP 200 with `{"status": "ok"}` when the app is healthy. It must not require authentication, log PII, or expose document text.
- Health/readiness exposes index freshness after RAG ingestion exists.

## Project-Specific Rules

### V1 Workspace Model

v1 is a single-company deployment per pilot. Records still carry `workspace_id`, but the project must not claim SaaS-grade multi-tenancy until an ADR defines RLS or separate database isolation and matching tests.

Violation: P1 for claiming multi-tenant security without ADR; P2 for adding workspace-scoped tables without workspace IDs.

### Human Approval Boundaries

AI feedback must not set final certification, manager approval, policy approval, sensitive-data exceptions, or productivity claims. Those fields are written only by human-approved routes.

Violation: automatic P1.

### Feedback Idempotency

Feedback jobs are idempotent by `(submission_id, submission_version)`. Retries update the existing job/feedback state and must not create duplicate feedback rows.

Violation: P1 if duplicate feedback can appear for one submission version.

### Artifact Retention And Redaction

Learner submissions and document bodies may be deleted or redacted according to retention settings, but audit events remain append-only. Redaction actions must record actor, reason, target, result, and trace ID.

Violation: P1 if redaction deletes audit evidence or leaves no audit event.

### Deterministic Metrics

Completion, submission, guardrail pass, manager approval, feedback backlog, sensitive-data flag rate, and report totals are computed from stored records. LLM output may summarize metrics but must not be the source of metric values.

Violation: P1 for LLM-owned manager-facing metric values.

### RAG Reference Reuse Boundary

The RAG implementation may adapt code and tests from `https://github.com/ashishki/Dream_Motif_Interpreter` according to `docs/reference/dream_motif_rag_reuse.md`. Reuse must preserve ingestion/query separation, `insufficient_evidence`, markdown-backed retrieval eval, stub-embedding test mode, pgvector schema versioning, and no-answer tests. Dream-domain models, symbolic dream query expansion, Telegram assistant logic, and motif/research behavior must not be copied into this project.

Violation: P1 if dream-domain behavior enters product code; P2 if reusable RAG safeguards are dropped without ADR.

### Codex-Only Execution Boundary

This project is operated by the current Codex session. Do not launch external AI worker processes, host-specific slash-command wrappers, or nested Codex CLI workers. Implementation, verification, review passes, state updates, and commits happen directly in the current workspace unless the human explicitly asks for parallel Codex subagents.

Violation: P1 if the workflow requires an external AI worker process to complete a normal task.

## Control Surface And Runtime Boundaries

| Boundary | Rule |
|----------|------|
| Secrets scope | Web and worker processes may read only the environment variables listed in `docs/ARCHITECTURE.md#runtime-contract`. |
| Network egress | Product code may call the configured LLM provider and explicitly enabled reminder/export integrations. Arbitrary runtime egress is forbidden. |
| Privileged actions | Certification, policy changes, approved examples, sensitive-data exceptions, and productivity claims require human-approved routes. |
| Runtime mutation | Product runtime must not install packages, alter services, execute shell commands, or mutate toolchains. |
| Persistence | PostgreSQL is the source of durable state. Worker-local memory is temporary and cannot be authoritative. |
| Auditability | Auth, denied access, submissions, policy snapshots, feedback jobs, approvals, exports, redaction, and report generation emit audit events. |

### Runtime Tier Guardrails

- Implement only within T1 as declared in `docs/ARCHITECTURE.md`.
- Runtime-tier expansion is a governance change and requires ADR.
- The project must not silently acquire T2/T3 behaviors such as broad shell mutation, privileged runtime management, or long-lived autonomous worker state.

## Profile Rules: RAG

Applies because `docs/ARCHITECTURE.md` declares RAG Status = ON.

### Corpus Isolation

- Every retrieval query is scoped to the active workspace and policy snapshot.
- Cross-workspace or cross-snapshot retrieval is a data leak and automatic P1.
- Corpus boundaries are enforced in retrieval SQL filters before evidence assembly.

### insufficient_evidence Path

- Every query-time handler implements `insufficient_evidence`.
- When evidence does not meet threshold or is stale, the system returns/stores `insufficient_evidence` instead of fabricated guidance.
- The path must have explicit integration tests.
- Omitting this path is automatic P1.

### Index Schema Versioning

- Index schema v1 covers embedding model, vector dimensions, chunking strategy, and metadata fields.
- Changing any schema parameter requires ADR and full re-index.
- Mixing chunks from incompatible schema versions in one active corpus is forbidden.

### Embedding Strategy Declaration

- Retrieval mode is text-only in v1.
- Preview or experimental embedding models are forbidden for manager-facing feedback without ADR, fallback model, and re-index plan.
- Changing retrieval mode, modalities, embedding provider/model, vector dimensions, or representation contract requires ADR and full re-index.

### Max Index Age

- Maximum active corpus index age is 7 days during a pilot.
- Health/readiness must expose index age after ingestion exists.
- Index age beyond 7 days is P2; beyond 14 days is P1 until refreshed or explicitly accepted by the human operator.

### Retrieval-Generation Separation

- Ingestion code lives under `ai_rollout_os/retrieval/ingestion.py`, chunking, embeddings, and repositories.
- Query-time code lives under `ai_rollout_os/retrieval/query.py` and evidence assembly modules.
- A single function or class must not mix ingestion and query-time behavior.
- Violation: P2.

### Retrieval Evaluation Gate

A task tagged `rag:ingestion` or `rag:query`, or a task touching chunking, embedding, ranking, evidence assembly, or `insufficient_evidence`, is not complete until:

1. `docs/retrieval_eval.md` is updated with current retrieval metrics or a valid not-yet-measured reason for pre-implementation bootstrap.
2. Metrics are compared to the baseline once a baseline exists.
3. Regression notes are filled when any metric declines.
4. Answer quality metrics are updated once feedback generation exists.
5. Evaluation History records Eval Source, Date, and Corpus Version.

Missing required evaluation evidence is P1 after the relevant implementation task begins.

### Retrieval Regression Policy

A retrieval metric regression in hit@k, MRR, citation precision, no-answer accuracy, or answer quality is P1 unless documented in `docs/retrieval_eval.md#regression-notes` and explicitly accepted by the human reviewer.

## Continuity And Retrieval Rules

- Canonical authority remains: `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/spec.md`, `docs/tasks.md`, `docs/CODEX_PROMPT.md`, ADRs, review reports, evaluation artifacts, code, and tests.
- `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, and `docs/EVIDENCE_INDEX.md` are retrieval aids. They never overrule canonical files.
- A task with `Context-Refs` must read those references before implementation begins.
- Retrieval is mandatory when changing architecture, runtime, auth, retrieval semantics, sensitive-data handling, migrations, or open review findings.
- If work supersedes a prior decision or invalidates evidence, update the retrieval artifact in the same task.

Violation: P2; repeated violation becomes P1 at age cap.

## Mandatory Pre-Task Protocol

Every Codex agent must execute these steps before writing implementation code:

1. Read the orchestrator's inline task digest first.
2. Read the full current task in `docs/tasks.md`, including acceptance criteria, Depends-On, Files, Context-Refs, and Notes.
3. Read all Depends-On tasks to understand interface contracts.
4. Read `docs/IMPLEMENTATION_CONTRACT.md` unless all applicable rules are inlined in the task digest.
5. Read task `Context-Refs` and relevant entries in `docs/DECISION_LOG.md`, `docs/IMPLEMENTATION_JOURNAL.md`, and `docs/EVIDENCE_INDEX.md` when the task depends on prior decisions, proof, or findings.
6. Run `pytest -q`. Record `{N} passing, {M} failed`. If `M > 0`, stop and report.
7. Run `ruff check`. It must exit 0. If not, fix lint in a separate commit, then restart this protocol.
8. Confirm every acceptance criterion has a corresponding test before implementation is considered done.

Skipping any step is P1 in the next review cycle.

## Forbidden Actions

| Forbidden Action | Reason |
|------------------|--------|
| String interpolation in SQL | SQL injection risk; parameterized queries are unconditional. |
| Skipping pre-task baseline capture | Cannot verify implementation did not break existing behavior. |
| Self-closing a review finding without showing the code change | Findings are verified by code review, not assertion. |
| Modifying this document without an ADR | The contract is immutable by design. |
| Deferring CI setup past Phase 1 | Every commit after baseline needs CI verification. |
| Merging with failing CI | CI is a non-negotiable gate. |
| Committing credentials or secrets | Irreversible exposure. |
| Expanding runtime tier or privilege surface without ADR | Runtime escalation is a governance change. |
| Treating retrieval surfaces as authority over canonical docs | Retrieval surfaces are convenience, not source of truth. |
| LLM-generated final certification or manager approval | Human accountability boundary. |
| Uncited policy guidance in feedback | RAG evidence boundary. |
| Leaving commented-out code in a commit | Dead code degrades review quality. |
| Adding a TODO without a task reference | Orphaned TODOs are not trackable. |

## Quality Process Rules

### P2 Age Cap

Any P2 finding open for more than 3 review cycles must be resolved, escalated to P1, or formally deferred to v2 with an ADR.

### Commit Granularity

One logical change per commit. Do not bundle unrelated migrations, service logic, tests, and documentation changes when they can be reviewed separately.

### Sandbox Isolation

Tests do not share mutable state. Database tests use transaction rollback or fresh isolated schemas. External API calls are faked unless an integration test explicitly declares a safe test endpoint.

### Evaluation Validity

Evaluation artifact entries are invalid if Eval Source or Date is absent. "Ran evaluation" without a command, script, or manual-check scope is not valid evidence.

### Review Cycle Integrity

Review agents close findings only after verifying the fix in code and tests.

## Governing Documents

| Document | Path | Role |
|----------|------|------|
| Architecture | `docs/ARCHITECTURE.md` | System design, profile, runtime, and boundary authority. |
| Specification | `docs/spec.md` | Product behavior and feature scope authority. |
| Task graph | `docs/tasks.md` | Implementation task authority. |
| Session handoff | `docs/CODEX_PROMPT.md` | Current state, next task, baseline, and findings authority. |
| This document | `docs/IMPLEMENTATION_CONTRACT.md` | Immutable implementation rule authority. |
| Decision log | `docs/DECISION_LOG.md` | Retrieval index for decisions. |
| Implementation journal | `docs/IMPLEMENTATION_JOURNAL.md` | Cross-session handoff surface. |
| Evidence index | `docs/EVIDENCE_INDEX.md` | Index for tests, evals, reviews, and proof artifacts. |
| Retrieval eval | `docs/retrieval_eval.md` | RAG evaluation lifecycle authority. |
| Review reports | `docs/audit/` | Finding authority. |
| ADRs | `docs/adr/` | Approved decision changes. |

Precedence order:

1. `docs/IMPLEMENTATION_CONTRACT.md`
2. `docs/adr/`
3. `docs/ARCHITECTURE.md`
4. `docs/spec.md`
5. `docs/tasks.md`
6. `docs/CODEX_PROMPT.md`
7. Retrieval convenience artifacts
