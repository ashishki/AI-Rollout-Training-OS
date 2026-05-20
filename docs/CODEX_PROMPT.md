# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-20
Phase: 8

This file is the single source of truth for session state. Update it at task and phase boundaries.

---

## Current State

- Phase: 8
- Baseline: 100 passing tests
- Ruff: `ruff check scripts ai_rollout_os frontend tests migrations` and `ruff format --check scripts ai_rollout_os frontend tests migrations` passing
- Last CI run: not yet configured
- Last updated: 2026-05-20
- Session tokens: not yet tracked
- Cumulative phase tokens: not yet tracked
- Execution model: Codex-only current session; no external AI worker process
- Development loop: nonstop; do not pause between phases when checks pass and no P0/P1 blockers remain

## Summary State

- Current phase: 8 Enterprise Security
- Current baseline: 100 passing tests
- Most recent task: T34 UX Readiness Gate
- Active next task: T35 SSO And Identity Boundary
- Planned MVP task graph: complete through T24
- Post-MVP production maturity graph: complete through T34; open from T35 through T61
- Recent phase boundary: Phase 7 UX audit conditionally passed with no open P0/P1 findings and one open P2 finding
- Older completed-task and phase rows are preserved in archive sections below.

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Retrieval evaluation: `docs/retrieval_eval.md`
- Codex-only workflow: `reference/CODEX_ONLY_WORKFLOW.md`
- MVP task graph: `docs/tasks.md`
- Post-MVP task graph: `docs/product_maturity_task_graph.md`
- Product maturity roadmap: `docs/product_maturity_roadmap.md`
- Task-scoped context: read `Context-Refs` in the active task graph before broad searching

## Next Task

T35: SSO And Identity Boundary

## Fix Queue

empty

## Open Findings

- P2-UX-001 (T34): Browser automation is not yet installed; current e2e coverage uses HTTP UI surfaces rather than a real browser rendering engine. Not blocking Phase 8, but required before claiming full UX readiness for GA-grade non-engineer operation.

## Profile State: RAG

- RAG Status: ON
- Active corpora: company policy, SOPs, role-pack content, rubrics, allowed/forbidden use cases, approved examples
- Retrieval mode: text-only
- Retrieval baseline: T22 automated text-only baseline measured
- Open retrieval findings: none
- Index schema version: v1 implemented
- Max index age: 7 days after ingestion exists
- Pending reindex actions: none
- Retrieval-related next tasks: none currently scheduled
- Retrieval-driven tasks: none
- Reuse reference: `docs/reference/dream_motif_rag_reuse.md`

## Tool-Use State

- Tool-Use Profile: OFF
- Registered tool schemas: n/a
- Unsafe-action guardrails: n/a
- Open tool findings: none

## Agentic State

- Agentic Profile: OFF
- Active agent roles: n/a
- Loop termination contract version: n/a
- Cross-iteration state mechanism: n/a
- Open agent findings: none

## Planning State

- Planning Profile: OFF
- Plan schema version: n/a
- Plan validation method: n/a
- Open plan findings: none

## Compliance State

- Compliance Status: OFF
- Active frameworks: n/a
- Controls implemented: n/a
- Controls partial: n/a
- Controls not started: n/a
- Evidence artifact: n/a
- Open compliance findings: none

## NFR Baseline

- API p99 latency: not yet measured
- Feedback p95 latency: target under 60 seconds, not yet measured
- Retrieval p95 latency: 92.19 ms in T22 local eval baseline
- Error rate: not yet measured
- Throughput: not yet measured
- Last measured: 2026-05-19 for retrieval eval latency
- NFR regression open: No

## Evaluation State

### Last Evaluation

- Profile: RAG
- Task: T22: Retrieval Evaluation Automation
- Date: 2026-05-19
- Eval Source: `scripts/eval.py against docs/retrieval_eval.md#evaluation-dataset`, run 2026-05-19
- Metric(s): hit@3=1.00; hit@5=1.00; MRR=0.94; citation_precision=0.58; no_answer_accuracy=1.00; median_latency_ms=61.83; p95_latency_ms=92.19
- Score: pass
- Baseline: T22 automated text-only eval baseline
- Delta: n/a
- Regression: No

### Open Evaluation Issues

none

### Evaluation History

| Date | Task | Profile | Key metric | Score | Baseline | Delta | Regression? |
|------|------|---------|------------|-------|----------|-------|-------------|
| 2026-05-19 | T22 | RAG | Automated retrieval eval | hit@3=1.00; hit@5=1.00; MRR=0.94; no_answer_accuracy=1.00 | first automated baseline | n/a | No |
| 2026-05-19 | T15 | RAG | Answer quality bootstrap | schema validation added; metrics not yet measured | n/a | n/a | No |
| 2026-05-19 | T14 | RAG | Query bootstrap | citation/no-answer proxies passed | n/a | n/a | No |
| 2026-05-19 | T13 | RAG | Ingestion bootstrap | n/a | n/a | n/a | No |

## Completed Tasks

| Date | Task | Summary | Evidence |
|------|------|---------|----------|
| 2026-05-20 | T34: UX Readiness Gate | Added the Phase 7 UX audit covering critical operator, learner, manager, and app-shell workflows. Conditional go to Phase 8 with one open P2 for missing browser automation. | `.venv/bin/pytest -q` -> 100 passed; `.venv/bin/ruff check scripts ai_rollout_os frontend tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os frontend tests migrations` -> passed |
| 2026-05-20 | T33: Manager Review UI | Added manager UI endpoints for filtered review queue, dashboard snapshot, workflow approval, and report creation; added e2e coverage for approval/report flow and manager-note non-leak behavior. | `.venv/bin/pytest -q` -> 99 passed; `.venv/bin/ruff check scripts ai_rollout_os frontend tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os frontend tests migrations` -> passed |
| 2026-05-20 | T32: Learner Mission UI | Added learner UI endpoints for assignments, guardrail quiz submission, artifact submission, feedback status surface, and redacted display for sensitive submissions. | `.venv/bin/pytest -q` -> 97 passed; `.venv/bin/ruff check scripts ai_rollout_os frontend tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os frontend tests migrations` -> passed |
| 2026-05-20 | T31: Operator Admin UI | Added operator admin UI form endpoints for policy/SOP documents, guardrail quizzes, role packs, missions, role-pack launch, cohort creation, and cohort launch; added e2e coverage proving an operator can launch a cohort and policy body text does not leak in UI errors/logs. | `.venv/bin/pytest -q` -> 95 passed; `.venv/bin/ruff check scripts ai_rollout_os frontend tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os frontend tests migrations` -> passed |
| 2026-05-20 | T30: Frontend Application Shell | Added authenticated `/app` frontend shell with role-specific operator, manager, and learner navigation; protected unknown/missing/invalid roles; added e2e coverage and included `frontend` in ruff/CI scope. | `.venv/bin/pytest -q` -> 93 passed; `.venv/bin/ruff check scripts ai_rollout_os frontend tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os frontend tests migrations` -> passed |
| 2026-05-20 | T29: Phase 6 PMF Gate | Added the Phase 6 PMF audit with evidence, gaps, and go/no-go status: conditional go for Phase 7 UX work, no-go for claiming PMF or paid expansion readiness until observed customer evidence meets the exit gate. | `.venv/bin/pytest -q` -> 91 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed |
| 2026-05-20 | T28: Pilot ROI Report | Added a conservative ROI report service that summarizes adoption, approved workflow changes, risk signals, denominator fields, and assumption-labeled manual review savings without productivity guarantees. | `.venv/bin/pytest -q` -> 90 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed |
| 2026-05-20 | T27: Pilot Success Rubric | Added a pilot go/no-go rubric defining expand, repeat, pause, and reposition outcomes with product, quality, and business metrics. | `.venv/bin/pytest -q` -> 88 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed |
| 2026-05-20 | T26: Customer Discovery Evidence Registry | Added a structured customer discovery registry for ICP, buyer, blockers, workarounds, willingness-to-pay signals, pilot outcome notes, confidence levels, interview templates, and decision rules that separate observed evidence from internal assumptions. | `.venv/bin/pytest -q` -> 86 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed |
| 2026-05-20 | T25: Pilot Outcome Metrics Model | Added deterministic pilot outcome metrics for activation, completion, approved workflow changes, manager review time, risk rate, and time-to-first-safe-use, plus explicit Phase 6 metrics and exit gate documentation. | `.venv/bin/pytest -q` -> 84 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T24: Pilot Readiness Gate | Added pilot readiness checklist, minimum pilot seed fixture, and end-to-end pilot test covering cohort launch, artifact submission, feedback generation, manager approval, and report export. | `.venv/bin/pytest -q` -> 79 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T23: Docker Compose Deployment | Added Dockerfile, Docker Compose web/migrate/worker/postgres services, `.env.example` placeholders, bounded worker runner command, default deployed DB session factory, and deployment file tests. | `.venv/bin/pytest -q` -> 76 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed; `docker-compose config` -> passed |
| 2026-05-19 | T22: Retrieval Evaluation Automation | Added CI-safe retrieval eval runner, seeded policy/SOP corpus fixture, automated hit@3/hit@5/MRR/citation/no-answer/latency metrics, no-write mode, and eval-history validation. | `.venv/bin/pytest -q` -> 73 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/python scripts/eval.py --no-write` -> pass |
| 2026-05-19 | T21: Reminder Scheduler | Added deterministic reminder job persistence, due-assignment reminder scheduling, idempotency by resource/reminder type, disabled-by-default delivery adapter behavior, and reminder audit events. | `.venv/bin/pytest -q` -> 68 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T20: Role Pack Version Iteration | Added role-pack version update and comparison endpoints, mission template version rollover, historical assignment preservation, changed rubric/guardrail diff metadata, and operator audit events. | `.venv/bin/pytest -q` -> 65 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |

## Archived Completed Tasks

| Date | Task | Summary | Evidence |
|------|------|---------|----------|
| 2026-05-19 | T19: Exportable Progress Reports | Added versioned progress report persistence, manager report creation route, dashboard metric snapshots, approved workflow changes and open risk flags in Markdown/JSON output, and report audit events without raw submission text. | `.venv/bin/pytest -q` -> 62 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T18: Dashboard Metrics | Added deterministic manager cohort dashboard endpoint with completion, submission, guardrail, approval, feedback backlog, sensitive-data flag metrics, denominator fields, and no-provider-call checks. | `.venv/bin/pytest -q` -> 59 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T17: Manager Review And Approval Workflow | Added manager submission queue filters, manager-only workflow approval route, approval fields and audit event, feedback-result risk flags, and tests proving feedback jobs cannot set approval fields. | `.venv/bin/pytest -q` -> 56 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T16: Feedback Background Jobs | Added PostgreSQL-backed feedback job/result tables, idempotent enqueue by submission/version, retryable single-job worker execution, timeout routing to human review, and job audit events. | `.venv/bin/pytest -q` -> 53 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T15: Rubric Evaluation Engine | Added structured feedback schema validation, citation validation against retrieved evidence, insufficient-evidence routing to human review, and feedback audit event. | `.venv/bin/pytest -q` -> 50 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T14: Retrieval Query And Evidence Assembly | Added query-side retrieval service, hybrid pgvector/FTS candidate retrieval, reciprocal rank fusion, workspace/snapshot/document-type filtering, citation evidence blocks, and `insufficient_evidence` behavior. | `.venv/bin/pytest -q` -> 47 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T13: Text Retrieval Ingestion Pipeline | Added section-aware token chunking, embedding adapter protocol, pgvector chunk storage, corpus version records, snapshot-preserving reingestion, and RAG eval bootstrap history. | `.venv/bin/pytest -q` -> 42 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T12: Sensitive Data Redaction Gate | Added deterministic sensitive-data detection for submissions, blocked flagged artifacts from feedback, redacted flagged response text, and added manager approval audit flow. | `.venv/bin/pytest -q` -> 36 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T11: Submission Storage And Review States | Added learner submission storage, assignment validation, per-assignment versioning, policy snapshot/rubric capture, review state, and submission audit events. | `.venv/bin/pytest -q` -> 33 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T10: Guardrail Quiz Engine | Added guardrail quiz creation, deterministic answer-key scoring, persisted quiz results, and mission feedback-release gating on passing quiz results. | `.venv/bin/pytest -q` -> 30 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T09: Cohorts And Enrollment | Added cohort, enrollment, and mission assignment models/routes with draft cohort creation, idempotent assignment generation, learner assignment access control, and denied-access audit. | `.venv/bin/pytest -q` -> 27 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T08: Policy Document Registry | Added operator-only versioned source document registry with snapshot IDs, update snapshots, prior snapshot lookup, safe logging, and audit events. | `.venv/bin/pytest -q` -> 24 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T07: Role Pack And Mission Models | Added role-pack, mission-template, rubric, and guardrail quiz schema/migration models plus operator APIs for draft role packs, missions, and launch validation. | `.venv/bin/pytest -q` -> 21 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T06: Authentication And Workspace Boundary | Added signed bearer tokens, actor request context, role/workspace authorization dependencies, and denied-access audit events. | `.venv/bin/pytest -q` -> 18 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T05: Database Migrations And Audit Ledger | Added SQLAlchemy models/session helpers, Alembic foundation migration, append-only audit repository, and PostgreSQL-backed integration tests. | `.venv/bin/pytest -q` -> 15 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed |
| 2026-05-19 | T04: Configuration And Observability Baseline | Added runtime env parsing, test defaults, PII-safe JSON logging, trace ID propagation, and shared tracer helper. | `.venv/bin/pytest -q` -> 12 passed; `.venv/bin/ruff check ai_rollout_os tests` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests` -> passed |
| 2026-05-19 | T03: First Smoke Tests | Added baseline smoke tests for pytest collection, ruff execution, and Codex state tracking. | `.venv/bin/pytest -q` -> 9 passed; `.venv/bin/ruff check ai_rollout_os tests` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests` -> passed |
| 2026-05-19 | T02: CI Setup | Tightened GitHub Actions CI and added tests for required Python, dependency, lint, format, pytest, pgvector service, and test-secret configuration. | `.venv/bin/pytest -q` -> 6 passed; `.venv/bin/ruff check ai_rollout_os tests` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests` -> passed |
| 2026-05-19 | T01: Project Skeleton | Created FastAPI package skeleton, health endpoint, dependency metadata, and initial tests. | `.venv/bin/pytest -q` -> 3 passed; `.venv/bin/ruff check ai_rollout_os tests` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests` -> passed |

## Phase History

| Date | Phase | Summary | Evidence | Open P0/P1 |
|------|-------|---------|----------|------------|
| 2026-05-20 | Phase 7 | Completed T30-T34 core product UX: authenticated role shell, operator admin UI, learner mission UI, manager review UI, and UX readiness gate. Conditional go to Phase 8; one P2 remains for missing browser automation. | `docs/audit/PHASE7_UX_AUDIT.md`; `.venv/bin/pytest -q` -> 100 passed; `.venv/bin/ruff check scripts ai_rollout_os frontend tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os frontend tests migrations` -> passed | 0 |
| 2026-05-20 | Phase 6 | Completed T25-T29 PMF pilot system: deterministic pilot metrics, discovery registry, success rubric, conservative ROI report, and PMF gate. Conditional go for Phase 7 UX work; PMF claim remains not met until observed customer evidence satisfies the exit gate. | `docs/audit/PHASE6_PMF_AUDIT.md`; `.venv/bin/pytest -q` -> 91 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed | 0 |
| 2026-05-19 | Phase 5 | Completed T21-T24 pilot readiness: reminders, automated retrieval eval, Docker Compose deployment assets, and pilot readiness end-to-end gate. | `docs/audit/PHASE5_AUDIT.md`; `.venv/bin/pytest -q` -> 79 passed; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` -> passed | 0 |
| 2026-05-19 | Phase 4 | Completed T16-T20 review, dashboard, reports, and iteration workflows: feedback jobs, manager approvals, dashboard metrics, exportable reports, and role-pack versioning. | `docs/audit/PHASE4_AUDIT.md`; `.venv/bin/pytest -q` -> 65 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed | 0 |

## Archived Phase History

| Date | Phase | Summary | Evidence | Open P0/P1 |
|------|-------|---------|----------|------------|
| 2026-05-19 | Phase 3 | Completed T11-T15 feedback foundation: submission storage, sensitive-data redaction, retrieval ingestion, retrieval query/evidence assembly, and structured feedback validation with human-review routing. | `docs/audit/PHASE3_AUDIT.md`; `.venv/bin/pytest -q` -> 50 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed | 0 |
| 2026-05-19 | Phase 2 | Completed T06-T10 training setup: auth/workspace boundary, role packs/missions, policy document registry, cohorts/enrollment, and deterministic guardrail quizzes. | `docs/audit/PHASE2_AUDIT.md`; `.venv/bin/pytest -q` -> 30 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed | 0 |
| 2026-05-19 | Phase 1 | Completed T01-T05 foundation: skeleton, CI, smoke baseline, config/observability, migrations, and append-only audit repository. | `docs/audit/PHASE1_AUDIT.md`; `.venv/bin/pytest -q` -> 15 passed; `.venv/bin/ruff check ai_rollout_os tests migrations` -> passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` -> passed | 0 |

## Compaction Protocol

Compact this file when either condition is true:

- `## Completed Tasks` contains more than 20 entries.
- `## Phase History` contains more than 5 phase summaries.

When compacting, create or update `## Summary State` immediately after `## Current State`, retain the 5 most recent completed tasks, retain the 2 most recent phase summaries, and move older entries to archive sections. Do not delete history.

## Instructions for Codex

1. Read the orchestrator's inline task digest first.
2. Read `docs/tasks.md` for the current task entry.
3. Read `docs/IMPLEMENTATION_CONTRACT.md` when the digest does not inline applicable rules or when the task touches a risky boundary.
4. Read Depends-On tasks, `Context-Refs`, and continuity artifacts when the task depends on prior decisions, proof, or findings.
5. Execute tasks directly in the current Codex session; do not launch an external AI worker process.
6. Run `pytest -q` before changing code and record the baseline. If tests fail, stop and report the blocker.
7. Run `ruff check`. It must exit 0 before implementation work proceeds. Fix lint in a separate commit if needed.
8. Write tests before or alongside implementation. Every acceptance criterion has at least one test.
9. For RAG tasks, update `docs/retrieval_eval.md` and this file's evaluation state before returning done.
10. Update this file at task completion: new baseline, completed task, next task, and any open findings.
11. Commit with format `type(scope): description`; one logical change per commit.
12. Continue the loop after each completed task and after each clean phase boundary; stop only for a true blocker, an unresolved P0/P1 finding, a required human decision, or an explicit human pause instruction.

## Return Format

When done, return exactly:

```text
IMPLEMENTATION_RESULT: DONE
New baseline: {N} passing tests
Commits: {list of commit hashes and messages}
Notes: {anything the orchestrator should know}
```

When blocked, return exactly:

```text
IMPLEMENTATION_RESULT: BLOCKED
Blocker: {exact blocker}
Type: dependency | interface_mismatch | environment | ambiguity
Recommended action: {what the orchestrator or human should do}
Progress made: {what was completed before the blocker}
```
