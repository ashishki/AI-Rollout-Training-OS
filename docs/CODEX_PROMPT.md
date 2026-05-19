# CODEX_PROMPT.md

Version: 1.0
Date: 2026-05-19
Phase: 5

This file is the single source of truth for session state. Update it at task and phase boundaries.

---

## Current State

- Phase: 5
- Baseline: 79 passing tests
- Ruff: `ruff check scripts ai_rollout_os tests migrations` and `ruff format --check scripts ai_rollout_os tests migrations` passing
- Last CI run: not yet configured
- Last updated: 2026-05-19
- Session tokens: not yet tracked
- Cumulative phase tokens: not yet tracked
- Execution model: Codex-only current session; no external AI worker process
- Development loop: nonstop; do not pause between phases when checks pass and no P0/P1 blockers remain

## Summary State

- Current phase: 5 pilot readiness
- Current baseline: 79 passing tests
- Most recent task: T24 Pilot Readiness Gate
- Active next task: none; planned task graph complete
- Recent phase boundary: Phase 5 audit passed with no open P0/P1/P2 findings
- Older completed-task and phase rows are preserved in archive sections below.

## Continuity Pointers

- Decision log: `docs/DECISION_LOG.md`
- Implementation journal: `docs/IMPLEMENTATION_JOURNAL.md`
- Evidence index: `docs/EVIDENCE_INDEX.md`
- Retrieval evaluation: `docs/retrieval_eval.md`
- Codex-only workflow: `reference/CODEX_ONLY_WORKFLOW.md`
- Task-scoped context: read `Context-Refs` in `docs/tasks.md` before broad searching

## Next Task

none; planned task graph complete

## Fix Queue

empty

## Open Findings

none

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
