# Implementation Journal - AI Rollout Training OS

Version: 1.0
Last updated: 2026-05-19
Status: append-only

This file is a retrieval surface and handoff log. Canonical docs remain the authority.

---

## Journal Entry Template

```markdown
### YYYY-MM-DD - TNN - Short Title

- Scope: files or directories changed
- Why this work happened: reason or trigger
- Decisions applied: Decision Log or ADR refs
- Evidence collected: tests, evals, review reports, manual checks
- Follow-ups: next task, open risk, or none
- Notes for next agent: only context worth carrying forward
```

## Entries

### 2026-05-19 - T24 - Pilot Readiness Gate

- Scope: `docs/pilot_readiness.md`, `tests/fixtures/pilot_data.py`, `tests/integration/test_pilot_readiness.py`, `tests/test_pilot_readiness_doc.py`
- Why this work happened: Orchestrator advanced to T24 after T23 completed.
- Decisions applied: `docs/ARCHITECTURE.md#problem-fit-and-adoption-reality`, `docs/spec.md#overview`, `docs/EVIDENCE_INDEX.md#evidence-table`
- Evidence collected: `.venv/bin/pytest -q` passed with 79 tests; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` passed.
- Follow-ups: Phase 5 audit; planned task graph complete.
- Notes for next agent: The pilot fixture seeds one operator, one manager, two learners, one active role pack, two missions, one guardrail quiz, one rubric, and policy/SOP documents. The end-to-end test launches a cohort, submits an artifact, runs bounded feedback generation through the job worker, records manager approval, and exports a report.

### 2026-05-19 - T23 - Docker Compose Deployment

- Scope: `Dockerfile`, `docker-compose.yml`, `.env.example`, `ai_rollout_os/jobs/runner.py`, `ai_rollout_os/main.py`, `pyproject.toml`, `requirements.txt`, `tests/test_deployment_files.py`, `.github/workflows/ci.yml`
- Why this work happened: Orchestrator advanced to T23 after T22 completed.
- Decisions applied: `docs/ARCHITECTURE.md#runtime-and-isolation-model`, `docs/IMPLEMENTATION_CONTRACT.md#control-surface-and-runtime-boundaries`, `docs/IMPLEMENTATION_CONTRACT.md#credentials-and-secrets`
- Evidence collected: `.venv/bin/pytest -q` passed with 76 tests; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` passed; `docker-compose config` passed with `.env.example` defaults.
- Follow-ups: T24 pilot readiness gate.
- Notes for next agent: Compose defines `postgres`, `migrate`, `web`, and `worker` services. The worker uses the same image as web and runs `python -m ai_rollout_os.jobs.runner --run-once`; the runner currently schedules reminders in a bounded transaction. `.env.example` contains placeholders only.

### 2026-05-19 - T22 - Retrieval Evaluation Automation

- Scope: `scripts/eval.py`, `tests/fixtures/seed_training_documents.json`, `tests/eval/test_retrieval_eval.py`, `tests/unit/test_eval_script.py`, `tests/test_retrieval_eval_doc.py`, `docs/retrieval_eval.md`
- Why this work happened: Orchestrator advanced to T22 after T21 completed.
- Decisions applied: `docs/IMPLEMENTATION_CONTRACT.md#retrieval-evaluation-gate`, `docs/reference/dream_motif_rag_reuse.md#source-files-to-study-during-implementation`, `docs/retrieval_eval.md#evaluation-validity-rule`
- Evidence collected: `.venv/bin/pytest -q` passed with 73 tests; `.venv/bin/ruff check scripts ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check scripts ai_rollout_os tests migrations` passed; `.venv/bin/python scripts/eval.py --no-write` passed with hit@3=1.00, hit@5=1.00, MRR=0.94, citation_precision=0.58, no_answer_accuracy=1.00.
- Follow-ups: T23 Docker Compose deployment.
- Notes for next agent: The eval runner upgrades the schema, seeds a synthetic policy/SOP corpus, uses deterministic test embeddings, supports `--no-write`, and writes valid Evaluation History rows with Eval Source, Date, and Corpus Version. Product retrieval remains snapshot-scoped; the eval runner queries each seeded snapshot and aggregates evidence for corpus-level metrics.

### 2026-05-19 - T21 - Reminder Scheduler

- Scope: `ai_rollout_os/jobs/reminders.py`, `ai_rollout_os/jobs/delivery.py`, `ai_rollout_os/db/models.py`, `migrations/versions/0011_reminders.py`, `tests/integration/test_reminders.py`, `ai_rollout_os/core/config.py`
- Why this work happened: Orchestrator advanced to T21 after the Phase 4 boundary audit passed.
- Decisions applied: `docs/ARCHITECTURE.md#external-integrations`, `docs/IMPLEMENTATION_CONTRACT.md#control-surface-and-runtime-boundaries`
- Evidence collected: `.venv/bin/pytest -q` passed with 68 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T22 retrieval evaluation automation.
- Notes for next agent: Reminder delivery is disabled by default through settings. The scheduler persists reminder jobs and audit events; due-assignment reminders are idempotent by `assignment_id` and reminder type. `0011_reminders.py` is used because T19 already owns `0010_reports.py`.

### 2026-05-19 - T20 - Role Pack Version Iteration

- Scope: `ai_rollout_os/training/versioning.py`, `ai_rollout_os/training/routes.py`, `tests/integration/test_role_pack_versions.py`
- Why this work happened: Orchestrator advanced to T20 after T19 completed.
- Decisions applied: `docs/ARCHITECTURE.md#runtime-and-isolation-model`, `docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries`
- Evidence collected: `.venv/bin/pytest -q` passed with 65 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: Phase 4 boundary audit, then T21 reminder scheduler.
- Notes for next agent: Updating a launched role pack increments the role-pack version, creates replacement active mission templates for changed missions, deactivates superseded mission templates, preserves existing cohort assignments on their original `role_pack_version`, and writes `role_pack.version_created` audit details with previous/new version and diff metadata. The comparison endpoint returns the latest audited version diff.

### 2026-05-19 - T19 - Exportable Progress Reports

- Scope: `ai_rollout_os/reporting/reports.py`, `ai_rollout_os/reporting/report_routes.py`, `ai_rollout_os/db/models.py`, `migrations/versions/0010_reports.py`, `tests/integration/test_reports.py`
- Why this work happened: Orchestrator advanced to T19 after T18 completed.
- Decisions applied: `docs/spec.md#feature-dashboard-and-reports`, `docs/EVIDENCE_INDEX.md#evidence-table`
- Evidence collected: `.venv/bin/pytest -q` passed with 62 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T20 role pack version iteration.
- Notes for next agent: Report generation stores versioned Markdown/JSON snapshots with dashboard metrics, approved workflow changes, policy snapshot ID, and open risk flags. It intentionally excludes raw learner submission body text and writes `report.created` audit events.

### 2026-05-19 - T18 - Dashboard Metrics

- Scope: `ai_rollout_os/reporting/dashboard.py`, `ai_rollout_os/reporting/routes.py`, `ai_rollout_os/main.py`, `tests/integration/test_dashboard.py`
- Why this work happened: Orchestrator advanced to T18 after T17 completed.
- Decisions applied: `docs/spec.md#feature-dashboard-and-reports`, `docs/ARCHITECTURE.md#deterministic-vs-llm-owned-subproblems`
- Evidence collected: `.venv/bin/pytest -q` passed with 59 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T19 exportable progress reports.
- Notes for next agent: Dashboard metrics are pure database-derived values. No LLM/provider/model path is imported or called. The response includes denominator fields for empty-cohort and auditability checks.

### 2026-05-19 - T17 - Manager Review And Approval Workflow

- Scope: `ai_rollout_os/submissions/review_routes.py`, `ai_rollout_os/submissions/review_service.py`, `ai_rollout_os/submissions/models.py`, `ai_rollout_os/db/models.py`, `migrations/versions/0009_manager_review.py`, `tests/integration/test_manager_review.py`
- Why this work happened: Orchestrator advanced to T17 after T16 completed.
- Decisions applied: `docs/spec.md#feature-manager-review-and-approvals`, `docs/ARCHITECTURE.md#human-approval-boundaries`, `docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries`
- Evidence collected: `.venv/bin/pytest -q` passed with 56 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T18 dashboard metrics.
- Notes for next agent: Approval fields are written only through the manager route/service. Feedback jobs can create feedback results and risk flags but do not mutate approval status, manager ID, approval timestamp, or approved workflow-change text.

### 2026-05-19 - T16 - Feedback Background Jobs

- Scope: `ai_rollout_os/jobs/`, `ai_rollout_os/feedback/jobs.py`, `ai_rollout_os/db/models.py`, `migrations/versions/0008_jobs.py`, `tests/integration/test_feedback_jobs.py`
- Why this work happened: Orchestrator advanced to Phase 4/T16 after the Phase 3 boundary audit passed.
- Decisions applied: `docs/ARCHITECTURE.md#runtime-and-isolation-model`, `docs/IMPLEMENTATION_CONTRACT.md#control-surface-and-runtime-boundaries`, `docs/IMPLEMENTATION_CONTRACT.md#feedback-idempotency`
- Evidence collected: `.venv/bin/pytest -q` passed with 53 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T17 manager review and approval workflow.
- Notes for next agent: Worker execution is bounded to `run_one`, not an agent loop. Jobs are idempotent by `submission_id:submission_version`; retryable failures update the same job attempt count; successful retries upsert one feedback result row; timeouts route the submission to `needs_human_review`.

### 2026-05-19 - T15 - Rubric Evaluation Engine

- Scope: `ai_rollout_os/feedback/`, `tests/unit/test_feedback_schema.py`, `tests/unit/test_feedback_validation.py`, `tests/integration/test_feedback_engine.py`, `docs/retrieval_eval.md`
- Why this work happened: Orchestrator advanced to T15 after T14 completed.
- Decisions applied: `docs/ARCHITECTURE.md#inference-model-strategy`, `docs/spec.md#feature-ai-assisted-rubric-feedback`, `docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries`
- Evidence collected: `.venv/bin/pytest -q` passed with 50 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: Phase 3 boundary audit, then T16 feedback background jobs.
- Notes for next agent: The engine does not call an LLM yet. It validates structured feedback against retrieved evidence and routes insufficient evidence to human review with no learner-facing policy guidance. It updates submission review state and writes a feedback audit event.

### 2026-05-19 - T14 - Retrieval Query And Evidence Assembly

- Scope: `ai_rollout_os/retrieval/query.py`, `ai_rollout_os/retrieval/evidence.py`, `ai_rollout_os/retrieval/vector_repository.py`, `tests/integration/test_retrieval_query.py`, `tests/unit/test_retrieval_query.py`, `docs/retrieval_eval.md`
- Why this work happened: Orchestrator advanced to T14 after T13 completed.
- Decisions applied: `docs/IMPLEMENTATION_CONTRACT.md#insufficient_evidence-path`, `docs/reference/dream_motif_rag_reuse.md#source-files-to-study-during-implementation`
- Evidence collected: `.venv/bin/pytest -q` passed with 47 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T15 rubric evaluation engine.
- Notes for next agent: Query service returns `evidence_found` with deterministic citation blocks or `insufficient_evidence` with no generated answer. Retrieval filters by workspace, snapshot, document type, schema version, and minimum score. Full dataset metrics remain deferred to T22.

### 2026-05-19 - T13 - Text Retrieval Ingestion Pipeline

- Scope: `ai_rollout_os/retrieval/chunking.py`, `ai_rollout_os/retrieval/embeddings.py`, `ai_rollout_os/retrieval/ingestion.py`, `ai_rollout_os/retrieval/vector_repository.py`, `ai_rollout_os/db/models.py`, `migrations/versions/0007_retrieval_chunks.py`, `docs/retrieval_eval.md`, retrieval ingestion tests
- Why this work happened: Orchestrator advanced to T13 after T12 completed.
- Decisions applied: `docs/IMPLEMENTATION_CONTRACT.md#profile-rules-rag`, `docs/reference/dream_motif_rag_reuse.md#source-files-to-study-during-implementation`
- Evidence collected: `.venv/bin/pytest -q` passed with 42 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T14 retrieval query and evidence assembly.
- Notes for next agent: Ingestion is deliberately separate from query-time retrieval. T13 stores pgvector embeddings, source IDs, snapshot IDs, section paths, index schema v1, and corpus version rows. Retrieval metrics are still not measured because T14 owns query behavior and T22 owns the eval runner.

### 2026-05-19 - T12 - Sensitive Data Redaction Gate

- Scope: `ai_rollout_os/submissions/`, `ai_rollout_os/audit/repository.py`, `tests/integration/test_redaction.py`
- Why this work happened: Orchestrator advanced to T12 after T11 completed.
- Decisions applied: `docs/IMPLEMENTATION_CONTRACT.md#pii-policy`, `docs/spec.md#feature-learner-submissions`
- Evidence collected: `.venv/bin/pytest -q` passed with 36 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T13 text retrieval ingestion pipeline.
- Notes for next agent: Submission redaction is deterministic and local only. Flagged submissions return redacted artifact text, remain blocked from feedback until manager approval, and do not expose flagged text through product logs/spans/metrics.

### 2026-05-19 - T11 - Submission Storage And Review States

- Scope: `ai_rollout_os/submissions/`, `ai_rollout_os/db/models.py`, `ai_rollout_os/main.py`, `migrations/versions/0006_submissions.py`, `tests/integration/test_submissions.py`
- Why this work happened: Orchestrator advanced to T11 after Phase 2 boundary passed.
- Decisions applied: `docs/spec.md#feature-learner-submissions`, `docs/ARCHITECTURE.md#learner-submission-and-feedback`
- Evidence collected: `.venv/bin/pytest -q` passed with 33 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T12 sensitive data redaction gate.
- Notes for next agent: Submissions store text and return it to the learner route, but no logs/spans/metrics are emitted. Redaction starts as `not_checked`; T12 owns deterministic sensitive-data blocking.

### 2026-05-19 - T10 - Guardrail Quiz Engine

- Scope: `ai_rollout_os/training/guardrail_*`, `ai_rollout_os/db/models.py`, `ai_rollout_os/main.py`, `migrations/versions/0005_guardrails.py`, `tests/integration/test_guardrails.py`
- Why this work happened: Orchestrator advanced to T10 after T09 completed.
- Decisions applied: `docs/spec.md#feature-guardrail-quizzes`, `docs/ARCHITECTURE.md#deterministic-vs-llm-owned-subproblems`
- Evidence collected: `.venv/bin/pytest -q` passed with 30 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: Phase 2 boundary audit, then T11 submission storage and review states.
- Notes for next agent: Guardrail scoring is deterministic from stored answer keys. No LLM/model path is involved. The feedback-release gate returns `guardrail_quiz_not_passed` until the learner has a passing stored quiz result for the mission quiz.

### 2026-05-19 - T09 - Cohorts And Enrollment

- Scope: `ai_rollout_os/training/cohort_*`, `ai_rollout_os/db/models.py`, `ai_rollout_os/main.py`, `migrations/versions/0004_cohorts.py`, `tests/integration/test_cohorts.py`
- Why this work happened: Orchestrator advanced to T09 after T08 completed.
- Decisions applied: `docs/spec.md#feature-cohorts-and-enrollment`, `docs/ARCHITECTURE.md#human-approval-boundaries`
- Evidence collected: `.venv/bin/pytest -q` passed with 27 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T10 guardrail quiz engine.
- Notes for next agent: Assignment generation is idempotent by cohort/learner/mission through service checks and a DB unique constraint. Learner assignment reads require learner role and enrollment; denied enrollment reads emit audit events.

### 2026-05-19 - T08 - Policy Document Registry

- Scope: `ai_rollout_os/retrieval/document_*`, `ai_rollout_os/db/models.py`, `ai_rollout_os/main.py`, `migrations/versions/0003_documents.py`, `tests/integration/test_documents.py`
- Why this work happened: Orchestrator advanced to T08 after T07 completed.
- Decisions applied: `docs/spec.md#feature-company-policy-and-sop-knowledge-base`, `docs/IMPLEMENTATION_CONTRACT.md#pii-policy`
- Evidence collected: `.venv/bin/pytest -q` passed with 24 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T09 cohorts and enrollment.
- Notes for next agent: Document registry stores raw body text for later ingestion but does not log body text. Create/update emits audit events keyed to snapshot IDs; chunking and vector indexing remain deferred to T13.

### 2026-05-19 - T07 - Role Pack And Mission Models

- Scope: `ai_rollout_os/training/`, `ai_rollout_os/db/models.py`, `ai_rollout_os/main.py`, `migrations/versions/0002_role_packs.py`, `tests/integration/test_role_packs.py`
- Why this work happened: Orchestrator advanced to T07 after T06 completed.
- Decisions applied: `docs/spec.md#feature-role-packs-and-missions`, `docs/ARCHITECTURE.md#data-flow`
- Evidence collected: `.venv/bin/pytest -q` passed with 21 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T08 policy document registry.
- Notes for next agent: Training routes are operator-only and service queries are workspace-scoped by actor context. T07 stores operator-provided data only; it does not generate mission content.

### 2026-05-19 - T06 - Authentication And Workspace Boundary

- Scope: `ai_rollout_os/auth/`, `ai_rollout_os/main.py`, `tests/integration/test_auth.py`
- Why this work happened: Orchestrator advanced to T06 after Phase 1 boundary passed.
- Decisions applied: `docs/ARCHITECTURE.md#security-boundaries`, `docs/IMPLEMENTATION_CONTRACT.md#authorization`
- Evidence collected: `.venv/bin/pytest -q` passed with 18 tests; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: T07 role pack and mission models.
- Notes for next agent: Auth is implemented as reusable FastAPI dependencies. Future routes should use `authenticate_request`, `require_role`, and `require_workspace_match` at the route/service boundary before sensitive reads or writes.

### 2026-05-19 - T05 - Database Migrations And Audit Ledger

- Scope: `ai_rollout_os/db/`, `ai_rollout_os/audit/`, `migrations/`, `tests/integration/`, dependency metadata
- Why this work happened: Orchestrator advanced to T05 after T04 completed.
- Decisions applied: `docs/ARCHITECTURE.md#component-table`, `docs/IMPLEMENTATION_CONTRACT.md#sql-safety`, `docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules`
- Evidence collected: `.venv/bin/pytest -q` passed with 15 tests against local `pgvector/pgvector:pg16`; `.venv/bin/ruff check ai_rollout_os tests migrations` passed; `.venv/bin/ruff format --check ai_rollout_os tests migrations` passed.
- Follow-ups: Phase 1 boundary audit, then T06 authentication and workspace boundary.
- Notes for next agent: Local database evidence used Docker container `ai-rollout-training-os-postgres` on port 5432 with test credentials.

### 2026-05-19 - T04 - Configuration And Observability Baseline

- Scope: `ai_rollout_os/core/config.py`, `ai_rollout_os/observability/`, `tests/unit/`, `tests/test_codex_prompt_state.py`, `docs/CODEX_PROMPT.md`
- Why this work happened: Orchestrator advanced to T04 after T03 completed.
- Decisions applied: `docs/ARCHITECTURE.md#observability`, `docs/IMPLEMENTATION_CONTRACT.md#pii-policy`
- Evidence collected: `.venv/bin/pytest -q` passed with 12 tests; `.venv/bin/ruff check ai_rollout_os tests` passed; `.venv/bin/ruff format --check ai_rollout_os tests` passed.
- Follow-ups: T05 database migrations and audit ledger.
- Notes for next agent: `get_settings()` keeps test-safe defaults so the app factory remains importable without real keys; explicit non-test `APP_ENV` enforces required runtime vars.

### 2026-05-19 - T03 - First Smoke Tests

- Scope: `tests/test_baseline.py`, `tests/test_codex_prompt_state.py`, `docs/CODEX_PROMPT.md`
- Why this work happened: Orchestrator advanced to T03 after T02 completed.
- Decisions applied: `docs/CODEX_PROMPT.md#current-state`, `docs/IMPLEMENTATION_CONTRACT.md#mandatory-pre-task-protocol`
- Evidence collected: `.venv/bin/pytest -q` passed with 9 tests; `.venv/bin/ruff check ai_rollout_os tests` passed; `.venv/bin/ruff format --check ai_rollout_os tests` passed.
- Follow-ups: T04 configuration and observability baseline.
- Notes for next agent: The smoke baseline uses `pytest --collect-only` inside the test to avoid recursively running the suite from within itself.

### 2026-05-19 - T02 - CI Setup

- Scope: `.github/workflows/ci.yml`, `tests/test_ci_workflow.py`
- Why this work happened: Orchestrator advanced to T02 after T01 completed.
- Decisions applied: `docs/ARCHITECTURE.md#tech-stack`, `docs/IMPLEMENTATION_CONTRACT.md#ci-gate`
- Evidence collected: `.venv/bin/pytest -q` passed with 6 tests; `.venv/bin/ruff check ai_rollout_os tests` passed; `.venv/bin/ruff format --check ai_rollout_os tests` passed.
- Follow-ups: T03 first smoke tests.
- Notes for next agent: CI now assumes T01 files exist and directly runs dependency install, ruff, format, pytest, and optional retrieval eval.

### 2026-05-19 - T01 - Project Skeleton

- Scope: `pyproject.toml`, `requirements*.txt`, `.gitignore`, `ai_rollout_os/`, `tests/`
- Why this work happened: Orchestrator selected T01 from `docs/CODEX_PROMPT.md`.
- Decisions applied: `docs/ARCHITECTURE.md#file-layout`, `docs/IMPLEMENTATION_CONTRACT.md#mandatory-pre-task-protocol`
- Evidence collected: `.venv/bin/pytest -q` passed with 3 tests; `.venv/bin/ruff check ai_rollout_os tests` passed; `.venv/bin/ruff format --check ai_rollout_os tests` passed.
- Follow-ups: T02 CI setup.
- Notes for next agent: Test tooling is installed in local `.venv`; initial pre-task baseline could not run before T01 because `pytest` and `ruff` were not installed yet.

### 2026-05-19 - BOOTSTRAP - Phase 1 Package

- Scope: `docs/`, `.github/workflows/ci.yml`, `docs/prompts/ORCHESTRATOR.md`
- Why this work happened: `/bootstrap-new` was run for a brand-new AI Rollout Training OS repository.
- Decisions applied: `D-001`, `D-002`, `D-003`, `D-004`, `D-005`, `D-006`
- Evidence collected: structural checks after generation; Phase 1 validation still pending.
- Follow-ups: run Phase 1 validation, then start Orchestrator at T01.
- Notes for next agent: RAG is active and text-only; Tool-Use, Agentic, Planning, and Compliance profiles are OFF.

### 2026-05-19 - DOCS - RAG Reuse Reference Added

- Scope: `docs/ARCHITECTURE.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/tasks.md`, `docs/reference/dream_motif_rag_reuse.md`, `docs/retrieval_eval.md`
- Why this work happened: Human identified `https://github.com/ashishki/Dream_Motif_Interpreter` as a ready RAG/eval reference.
- Decisions applied: `D-007`
- Evidence collected: source repo inspection of `app/retrieval/*`, `scripts/eval.py`, `docs/retrieval_eval.md`, RAG tests, and pgvector migrations.
- Follow-ups: T13/T14/T22 should adapt the referenced implementation instead of designing retrieval from scratch.
- Notes for next agent: Preserve RAG safeguards and eval lifecycle; strip dream-domain query expansion and motif/Telegram logic.

### 2026-05-19 - DOCS - Codex-Only Execution Model

- Scope: `docs/prompts/ORCHESTRATOR.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/CODEX_PROMPT.md`, `reference/CODEX_ONLY_WORKFLOW.md`, legacy slash-command templates, local hooks`
- Why this work happened: Human clarified the project will use only the current Codex session and must not rely on nested Codex worker commands.
- Decisions applied: `D-008`
- Evidence collected: repository text scan for obsolete command placeholders and legacy operational paths.
- Follow-ups: future orchestration starts from `docs/prompts/ORCHESTRATOR.md` in the current Codex session.
- Notes for next agent: Do not reintroduce external AI worker commands into active project docs.

### 2026-05-19 - DOCS - Nonstop Development Loop

- Scope: `docs/prompts/ORCHESTRATOR.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/CODEX_PROMPT.md`, `reference/CODEX_ONLY_WORKFLOW.md`, `PLAYBOOK.md`
- Why this work happened: Human clarified that development must not pause between phases and must follow the loop continuously.
- Decisions applied: `D-009`
- Evidence collected: documentation scan for loop and phase-boundary rules.
- Follow-ups: future implementation sessions should continue from task to task and phase to phase unless a blocker, P0/P1 finding, or explicit pause instruction exists.
- Notes for next agent: Treat phase gates as in-loop checkpoints, not idle waiting states.
