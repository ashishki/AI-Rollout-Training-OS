# Evidence Index - AI Rollout Training OS

Version: 1.0
Last updated: 2026-05-19

This file indexes durable proof so agents can retrieve evidence quickly. It is not authoritative by itself. Every row must point to an actual artifact that carries the evidence.

---

## When To Use

Use this file because the project has active RAG evaluation artifacts, heavy tasks, and audit evidence needs.

## Evidence Table

| Topic / Finding / Task | Artifact type | Location | Scope covered | Last verified | Canonical? |
|------------------------|---------------|----------|---------------|---------------|------------|
| Phase 1 architecture package | planning docs | `docs/ARCHITECTURE.md`, `docs/spec.md`, `docs/tasks.md`, `docs/IMPLEMENTATION_CONTRACT.md` | Initial solution shape, runtime, profile status, and task graph | 2026-05-19 | Yes |
| RAG evaluation lifecycle | eval | `docs/retrieval_eval.md` | Retrieval dataset, metrics, no-answer behavior, and evaluation history | 2026-05-19 | Yes |
| RAG implementation reuse | reference | `docs/reference/dream_motif_rag_reuse.md` | Source repo files and adaptation constraints for RAG ingestion, query, eval, and pgvector migrations | 2026-05-19 | No |
| Codex-only workflow | reference | `reference/CODEX_ONLY_WORKFLOW.md`, `docs/prompts/ORCHESTRATOR.md` | Active execution model excludes external AI worker commands | 2026-05-19 | Yes |
| Nonstop development loop | governance rule | `docs/prompts/ORCHESTRATOR.md`, `docs/IMPLEMENTATION_CONTRACT.md`, `docs/DECISION_LOG.md#decision-index` | Codex continues across clean task and phase boundaries without waiting for a separate continue prompt | 2026-05-19 | Yes |
| Product maturity AI loop | roadmap + task graph + tests | `docs/product_maturity_roadmap.md`, `docs/product_maturity_task_graph.md`, `tests/test_product_maturity_docs.py` | Post-MVP phases 6-14, T25-T61 AI-loop task graph, production-readiness market strategy, and prompt/state wiring checks | 2026-05-19 | Yes |
| T01 project skeleton | tests | `tests/test_health.py`, `tests/test_app_factory.py`, `tests/test_project_metadata.py` | Health endpoint, FastAPI app factory import, pyproject metadata, pytest config, and ruff config | 2026-05-19 | Yes |
| T02 CI setup | tests | `tests/test_ci_workflow.py`, `.github/workflows/ci.yml` | GitHub Actions install, lint, format, pytest, PostgreSQL pgvector service, safe test env vars, and production-secret guard | 2026-05-19 | Yes |
| T03 smoke baseline | tests | `tests/test_baseline.py`, `tests/test_codex_prompt_state.py`, `docs/CODEX_PROMPT.md` | Local pytest collection, ruff command viability, and Codex baseline/next-task state | 2026-05-19 | Yes |
| T04 config and observability | tests | `tests/unit/test_config.py`, `tests/unit/test_logging.py`, `tests/unit/test_tracing.py` | Required-env validation, secret-safe errors, PII redaction, trace ID propagation, and shared tracer factory | 2026-05-19 | Yes |
| T05 database and audit ledger | tests | `tests/integration/test_migrations.py`, `tests/integration/test_audit_repository.py`, `migrations/versions/0001_foundation.py` | Alembic foundation tables, PostgreSQL migration execution, append-only audit event persistence, and no repository mutation methods | 2026-05-19 | Yes |
| T06 authentication and workspace boundary | tests | `tests/integration/test_auth.py`, `ai_rollout_os/auth/` | Signed bearer auth, actor context propagation, role denial audit, and workspace mismatch denial before mutation | 2026-05-19 | Yes |
| T07 role packs and missions | tests | `tests/integration/test_role_packs.py`, `migrations/versions/0002_role_packs.py`, `ai_rollout_os/training/` | Draft role pack creation, mission-template persistence, role-pack launch guard, operator auth, and workspace-scoped service queries | 2026-05-19 | Yes |
| T08 policy document registry | tests | `tests/integration/test_documents.py`, `migrations/versions/0003_documents.py`, `ai_rollout_os/retrieval/document_*` | Source document snapshot creation, update snapshot versioning, previous snapshot lookup, body-text log exclusion, and document audit events | 2026-05-19 | Yes |
| T09 cohorts and enrollment | tests | `tests/integration/test_cohorts.py`, `migrations/versions/0004_cohorts.py`, `ai_rollout_os/training/cohort_*` | Draft cohort creation, enrollment persistence, idempotent launch assignment generation, learner enrollment authorization, and denied-access audit | 2026-05-19 | Yes |
| T10 guardrail quiz engine | tests | `tests/integration/test_guardrails.py`, `migrations/versions/0005_guardrails.py`, `ai_rollout_os/training/guardrail_*` | Guardrail quiz persistence, deterministic answer-key scoring, quiz-result storage, and feedback-release gating on passing quiz result | 2026-05-19 | Yes |
| T11 submission storage | tests | `tests/integration/test_submissions.py`, `migrations/versions/0006_submissions.py`, `ai_rollout_os/submissions/` | Learner submission creation, assignment validation, policy snapshot/rubric capture, per-assignment versioning, review state, and submission audit events | 2026-05-19 | Yes |
| T12 sensitive data redaction | tests | `tests/integration/test_redaction.py`, `ai_rollout_os/submissions/redaction.py`, `ai_rollout_os/submissions/service.py` | Deterministic sensitive text detection, flagged submission blocking, response redaction, manager approval audit, and observability exclusion for flagged text | 2026-05-19 | Yes |
| T13 retrieval ingestion | tests + eval | `tests/integration/test_retrieval_ingestion.py`, `tests/unit/test_retrieval_ingestion.py`, `tests/test_retrieval_eval_doc.py`, `migrations/versions/0007_retrieval_chunks.py`, `docs/retrieval_eval.md` | Section-aware token chunking, ingestion/query import separation, pgvector chunk storage, corpus versioning, snapshot-preserving reingestion, and eval bootstrap status | 2026-05-19 | Yes |
| T14 retrieval query | tests + eval | `tests/integration/test_retrieval_query.py`, `tests/unit/test_retrieval_query.py`, `ai_rollout_os/retrieval/query.py`, `ai_rollout_os/retrieval/evidence.py`, `docs/retrieval_eval.md` | Hybrid pgvector/FTS retrieval, RRF fusion, workspace/snapshot/document-type filters, minimum score gating, citation evidence fields, and `insufficient_evidence` behavior | 2026-05-19 | Yes |
| T15 rubric feedback validation | tests + audit | `tests/unit/test_feedback_schema.py`, `tests/unit/test_feedback_validation.py`, `tests/integration/test_feedback_engine.py`, `ai_rollout_os/feedback/` | Structured feedback schema requirements, citation validation against assembled evidence, insufficient-evidence human-review routing, and feedback audit event | 2026-05-19 | Yes |
| T16 feedback background jobs | tests + migration | `tests/integration/test_feedback_jobs.py`, `migrations/versions/0008_jobs.py`, `ai_rollout_os/jobs/`, `ai_rollout_os/feedback/jobs.py` | Feedback job/result persistence, idempotent enqueue by submission version, retry attempt updates, duplicate feedback-result prevention, timeout human-review routing, and job audit events | 2026-05-19 | Yes |
| T17 manager review approvals | tests + migration | `tests/integration/test_manager_review.py`, `migrations/versions/0009_manager_review.py`, `ai_rollout_os/submissions/review_*` | Manager queue filters, guardrail/feedback/risk filtering, human-owned workflow approval fields, approval audit event, and feedback-job approval separation | 2026-05-19 | Yes |
| T18 dashboard metrics | tests | `tests/integration/test_dashboard.py`, `ai_rollout_os/reporting/dashboard.py`, `ai_rollout_os/reporting/routes.py` | Deterministic cohort dashboard rates/counts, denominator fields, empty-cohort zero metrics, and no LLM/provider call path | 2026-05-19 | Yes |
| T19 progress reports | tests + migration | `tests/integration/test_reports.py`, `migrations/versions/0010_reports.py`, `ai_rollout_os/reporting/reports.py`, `ai_rollout_os/reporting/report_routes.py` | Versioned report persistence, cohort metadata, role-pack version, policy snapshot, dashboard metric snapshot, approved workflow changes, open risk flags, raw-submission exclusion, and report audit event | 2026-05-19 | Yes |
| T20 role pack version iteration | tests + audit | `tests/integration/test_role_pack_versions.py`, `ai_rollout_os/training/versioning.py`, `ai_rollout_os/training/routes.py` | Launched role-pack version increments, changed mission template rollover, existing assignment version preservation, changed rubric/guardrail quiz diff metadata, and operator version audit event | 2026-05-19 | Yes |
| Phase 4 implementation audit | audit | `docs/audit/PHASE4_AUDIT.md`, `docs/audit/AUDIT_INDEX.md` | Phase 4 boundary review after T16-T20 with feedback jobs, manager approval boundary, dashboard/report determinism, role-pack versioning, SQL, PII, audit, and runtime-tier checks | 2026-05-19 | Yes |
| T21 reminder scheduler | tests + migration | `tests/integration/test_reminders.py`, `migrations/versions/0011_reminders.py`, `ai_rollout_os/jobs/reminders.py`, `ai_rollout_os/jobs/delivery.py` | Due-assignment reminder job creation, idempotency by assignment/reminder type, disabled-by-default delivery without external calls, and reminder audit events | 2026-05-19 | Yes |
| T22 retrieval evaluation automation | tests + eval | `scripts/eval.py`, `tests/eval/test_retrieval_eval.py`, `tests/unit/test_eval_script.py`, `tests/fixtures/seed_training_documents.json`, `docs/retrieval_eval.md` | Automated hit@3, hit@5, MRR, citation precision, no-answer accuracy, citation-field presence, retrieval latency, no-write eval mode, deterministic stub embeddings, and valid eval-history rows | 2026-05-19 | Yes |
| T23 Docker Compose deployment | tests + deployment config | `Dockerfile`, `docker-compose.yml`, `.env.example`, `tests/test_deployment_files.py`, `ai_rollout_os/jobs/runner.py` | Web, worker, migration, and PostgreSQL/pgvector services; bounded worker command; placeholder-only env example; `docker-compose config` validation | 2026-05-19 | Yes |
| T24 pilot readiness gate | tests + doc | `tests/integration/test_pilot_readiness.py`, `tests/fixtures/pilot_data.py`, `tests/test_pilot_readiness_doc.py`, `docs/pilot_readiness.md` | Minimum pilot fixture and end-to-end pilot path from cohort launch through submission, feedback generation, manager approval, and report export | 2026-05-19 | Yes |
| Phase 5 implementation audit | audit | `docs/audit/PHASE5_AUDIT.md`, `docs/audit/AUDIT_INDEX.md` | Phase 5 boundary review after T21-T24 with reminders, retrieval eval, deployment config, pilot readiness, runtime-tier, PII, SQL, and eval checks | 2026-05-19 | Yes |
| Phase 3 implementation audit | audit | `docs/audit/PHASE3_AUDIT.md`, `docs/audit/AUDIT_INDEX.md` | Phase 3 boundary review after T11-T15 with submissions, redaction, RAG ingestion/query, feedback validation, SQL, PII, eval, approval-boundary, and runtime-tier checks | 2026-05-19 | Yes |
| Phase 2 implementation audit | audit | `docs/audit/PHASE2_AUDIT.md`, `docs/audit/AUDIT_INDEX.md` | Phase 2 boundary review after T06-T10 with tests, lint, format, auth, SQL, secrets, PII, deterministic ownership, and runtime-tier checks | 2026-05-19 | Yes |
| Phase 1 implementation audit | audit | `docs/audit/PHASE1_AUDIT.md`, `docs/audit/AUDIT_INDEX.md` | Phase 1 boundary review after T01-T05 with tests, lint, format, SQL/secrets/runtime/audit checks | 2026-05-19 | Yes |
| Audit prompt set | review prompt | `docs/audit/` | Review cycle prompts and audit index | 2026-05-19 | Yes |
| Bootstrap handoff | journal note | `docs/IMPLEMENTATION_JOURNAL.md#entries` | Why the bootstrap package exists and next actions | 2026-05-19 | No |

## Retrieval Rules

- Prefer rows matching the current task's `Context-Refs`, open findings, or active profile tags.
- If an evidence row points to a stale or missing artifact, fix the artifact or remove the row.
- Do not treat a journal note as proof when a test, eval, or review report exists.
