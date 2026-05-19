# Task Graph - AI Rollout Training OS

Version: 1.0
Last updated: 2026-05-19

---

## Phase 1 - Foundation

Goal: establish the Python service skeleton, CI, first tests, configuration, observability, database migrations, and append-only audit base.

## T01: Project Skeleton

Owner:      codex
Phase:      1
Type:       none
Depends-On: none

Objective: |
  Create the Python package skeleton, dependency files, FastAPI app factory, health endpoint, local configuration entry points, and empty module boundaries described in docs/ARCHITECTURE.md.

Acceptance-Criteria:
  - id: AC-1
    description: "GET /health returns HTTP 200 with body containing status='ok' and service='ai-rollout-training-os'."
    test: "tests/test_health.py::test_health_endpoint_returns_ok"
  - id: AC-2
    description: "Importing ai_rollout_os.main:create_app returns a FastAPI instance without reading network resources or requiring real API keys."
    test: "tests/test_app_factory.py::test_create_app_without_external_resources"
  - id: AC-3
    description: "pyproject.toml declares package name, Python 3.12 support, ruff configuration, and pytest testpaths."
    test: "tests/test_project_metadata.py::test_pyproject_declares_required_metadata"

Files:
  - pyproject.toml
  - requirements.txt
  - requirements-dev.txt
  - .gitignore
  - ai_rollout_os/__init__.py
  - ai_rollout_os/main.py
  - ai_rollout_os/core/config.py
  - tests/test_health.py
  - tests/test_app_factory.py
  - tests/test_project_metadata.py

Context-Refs:
  - docs/ARCHITECTURE.md#file-layout
  - docs/IMPLEMENTATION_CONTRACT.md#mandatory-pre-task-protocol

Notes: |
  Keep the skeleton minimal. Do not add auth, database models, retrieval, or feedback logic in this task.

## T02: CI Setup

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01

Objective: |
  Wire GitHub Actions to install dependencies, run ruff lint, run ruff format checks, start PostgreSQL with pgvector for tests, and run pytest with safe test environment variables.

Acceptance-Criteria:
  - id: AC-1
    description: ".github/workflows/ci.yml contains checkout, Python 3.12 setup, dependency install, ruff check, ruff format --check, and pytest steps."
    test: "tests/test_ci_workflow.py::test_ci_workflow_has_required_steps"
  - id: AC-2
    description: ".github/workflows/ci.yml defines a PostgreSQL pgvector service with test credentials and a DATABASE_URL used by pytest."
    test: "tests/test_ci_workflow.py::test_ci_workflow_declares_pgvector_service"
  - id: AC-3
    description: "The CI workflow contains no literal production secret values; only test placeholders or GitHub secret references are present."
    test: "tests/test_ci_workflow.py::test_ci_workflow_has_no_production_secrets"

Files:
  - .github/workflows/ci.yml
  - tests/test_ci_workflow.py

Context-Refs:
  - docs/ARCHITECTURE.md#tech-stack
  - docs/IMPLEMENTATION_CONTRACT.md#ci-gate

Notes: |
  The generated bootstrap workflow may need tightening after T01 creates dependency files. Keep CI aligned with the package layout from T01.

## T03: First Smoke Tests

Owner:      codex
Phase:      1
Type:       none
Depends-On: T01, T02

Objective: |
  Establish the first passing test baseline for the skeleton and document the baseline in docs/CODEX_PROMPT.md.

Acceptance-Criteria:
  - id: AC-1
    description: "python -m pytest tests/ -q exits with status 0 and at least three tests collected."
    test: "tests/test_baseline.py::test_pytest_collects_initial_suite"
  - id: AC-2
    description: "ruff check ai_rollout_os/ tests/ exits with status 0."
    test: "tests/test_baseline.py::test_ruff_check_command_succeeds"
  - id: AC-3
    description: "docs/CODEX_PROMPT.md records the current passing-test count and sets Next Task to T04."
    test: "tests/test_codex_prompt_state.py::test_codex_prompt_records_initial_baseline"

Files:
  - tests/test_baseline.py
  - tests/test_codex_prompt_state.py
  - docs/CODEX_PROMPT.md

Context-Refs:
  - docs/CODEX_PROMPT.md#current-state
  - docs/IMPLEMENTATION_CONTRACT.md#mandatory-pre-task-protocol

Notes: |
  This task updates state only after tests and ruff pass locally.

## T04: Configuration And Observability Baseline

Owner:      codex
Phase:      1
Type:       none
Depends-On: T03

Objective: |
  Implement environment parsing, safe defaults for tests, structured logging helpers, trace ID propagation, and PII-safe observability primitives.

Acceptance-Criteria:
  - id: AC-1
    description: "Missing required runtime variables outside test mode raises a ConfigError listing variable names without secret values."
    test: "tests/unit/test_config.py::test_missing_required_env_reports_names_only"
  - id: AC-2
    description: "The logging formatter redacts email addresses and learner submission text fields from log records."
    test: "tests/unit/test_logging.py::test_logging_formatter_redacts_sensitive_fields"
  - id: AC-3
    description: "get_tracer returns a shared tracer object from ai_rollout_os.observability.tracing and callers do not instantiate inline tracers."
    test: "tests/unit/test_tracing.py::test_shared_tracer_factory_is_used"

Files:
  - ai_rollout_os/core/config.py
  - ai_rollout_os/observability/__init__.py
  - ai_rollout_os/observability/logging.py
  - ai_rollout_os/observability/tracing.py
  - tests/unit/test_config.py
  - tests/unit/test_logging.py
  - tests/unit/test_tracing.py

Context-Refs:
  - docs/ARCHITECTURE.md#observability
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

Notes: |
  Do not log learner artifact text, policy body text, full names, emails, or API keys.

## T05: Database Migrations And Audit Ledger

Owner:      codex
Phase:      1
Type:       none
Depends-On: T04

Objective: |
  Add SQLAlchemy session management, Alembic migrations, base tables for users/workspaces, and an append-only audit_events table used by later tasks.

Acceptance-Criteria:
  - id: AC-1
    description: "Alembic upgrade head creates users, workspaces, and audit_events tables in an empty PostgreSQL database."
    test: "tests/integration/test_migrations.py::test_alembic_upgrade_creates_foundation_tables"
  - id: AC-2
    description: "AuditEventRepository.append stores timestamp, actor_id, action, resource_type, resource_id, result, and trace_id."
    test: "tests/integration/test_audit_repository.py::test_append_audit_event_persists_required_fields"
  - id: AC-3
    description: "Application repository code exposes no delete or update method for audit_events records."
    test: "tests/integration/test_audit_repository.py::test_audit_repository_has_no_mutation_methods"

Files:
  - ai_rollout_os/db/__init__.py
  - ai_rollout_os/db/session.py
  - ai_rollout_os/db/models.py
  - ai_rollout_os/audit/__init__.py
  - ai_rollout_os/audit/repository.py
  - migrations/env.py
  - migrations/versions/0001_foundation.py
  - tests/integration/test_migrations.py
  - tests/integration/test_audit_repository.py

Context-Refs:
  - docs/ARCHITECTURE.md#component-table
  - docs/IMPLEMENTATION_CONTRACT.md#sql-safety
  - docs/IMPLEMENTATION_CONTRACT.md#project-specific-rules

Notes: |
  Use parameterized SQL or SQLAlchemy expressions only. Keep deletion/redaction of user artifacts separate from audit event immutability.

Execution-Mode: heavy
Evidence:
  - tests/integration/test_migrations.py::test_alembic_upgrade_creates_foundation_tables
  - tests/integration/test_audit_repository.py::test_audit_repository_has_no_mutation_methods
Verifier-Focus: |
  Confirm audit event records cannot be modified through application repository APIs and that migration rollback does not imply runtime deletion behavior.

## Phase 2 - Training Setup

Goal: implement authenticated operator/manager/learner boundaries, role packs, policy registry, cohorts, enrollment, and deterministic guardrail quizzes.

## T06: Authentication And Workspace Boundary

Owner:      codex
Phase:      2
Type:       none
Depends-On: T05

Objective: |
  Implement simple v1 authentication, role authorization, workspace-scoped record checks, and audit events for login and denied access.

Acceptance-Criteria:
  - id: AC-1
    description: "Authenticated requests include actor_id, role, workspace_id, and trace_id in request state."
    test: "tests/integration/test_auth.py::test_authenticated_request_sets_actor_context"
  - id: AC-2
    description: "A learner request to an operator-only route returns HTTP 403 and writes a denied_access audit event."
    test: "tests/integration/test_auth.py::test_role_denial_returns_403_and_audits"
  - id: AC-3
    description: "A request for a workspace_id different from the actor context returns HTTP 403 before database mutation."
    test: "tests/integration/test_auth.py::test_workspace_mismatch_denied_before_mutation"

Files:
  - ai_rollout_os/auth/__init__.py
  - ai_rollout_os/auth/dependencies.py
  - ai_rollout_os/auth/tokens.py
  - ai_rollout_os/auth/permissions.py
  - ai_rollout_os/main.py
  - tests/integration/test_auth.py

Context-Refs:
  - docs/ARCHITECTURE.md#security-boundaries
  - docs/IMPLEMENTATION_CONTRACT.md#authorization

Notes: |
  v1 is single-company per deployment, but records still carry workspace_id. Do not claim SaaS-grade tenant isolation.

Execution-Mode: heavy
Evidence:
  - tests/integration/test_auth.py::test_role_denial_returns_403_and_audits
  - tests/integration/test_auth.py::test_workspace_mismatch_denied_before_mutation
Verifier-Focus: |
  Confirm authorization gates run before any sensitive read or write path and that denied access is auditable without logging PII.

## T07: Role Pack And Mission Models

Owner:      codex
Phase:      2
Type:       none
Depends-On: T06

Objective: |
  Implement role-pack, mission-template, rubric, and versioning models plus operator APIs for creating draft role packs.

Acceptance-Criteria:
  - id: AC-1
    description: "POST /role-packs stores a draft role pack with role, title, version=1, and inactive launch status."
    test: "tests/integration/test_role_packs.py::test_create_draft_role_pack"
  - id: AC-2
    description: "POST /role-packs/{id}/missions stores mission objective, instructions, artifact type, rubric ID, and guardrail quiz ID."
    test: "tests/integration/test_role_packs.py::test_add_mission_to_role_pack"
  - id: AC-3
    description: "Launching a role pack with zero active missions returns HTTP 409 with code role_pack_has_no_missions."
    test: "tests/integration/test_role_packs.py::test_launch_requires_active_mission"

Files:
  - ai_rollout_os/training/models.py
  - ai_rollout_os/training/schemas.py
  - ai_rollout_os/training/routes.py
  - ai_rollout_os/training/service.py
  - migrations/versions/0002_role_packs.py
  - tests/integration/test_role_packs.py

Context-Refs:
  - docs/spec.md#feature-role-packs-and-missions
  - docs/ARCHITECTURE.md#data-flow

Notes: |
  Do not generate mission content with AI in this task. Store operator-provided data only.

## T08: Policy Document Registry

Owner:      codex
Phase:      2
Type:       none
Depends-On: T06

Objective: |
  Implement operator APIs and database models for registering company policy, SOP, allowed-use, forbidden-use, and approved-example text documents before retrieval ingestion.

Acceptance-Criteria:
  - id: AC-1
    description: "POST /documents stores title, document_type, body text, effective_date, workspace_id, and snapshot_id."
    test: "tests/integration/test_documents.py::test_create_policy_document_snapshot"
  - id: AC-2
    description: "Updating a document creates a new snapshot_id and leaves the previous snapshot queryable."
    test: "tests/integration/test_documents.py::test_document_update_creates_new_snapshot"
  - id: AC-3
    description: "Document body text never appears in INFO-level logs during create or update requests."
    test: "tests/integration/test_documents.py::test_document_body_not_logged"

Files:
  - ai_rollout_os/retrieval/document_models.py
  - ai_rollout_os/retrieval/document_routes.py
  - ai_rollout_os/retrieval/document_service.py
  - migrations/versions/0003_documents.py
  - tests/integration/test_documents.py

Context-Refs:
  - docs/spec.md#feature-company-policy-and-sop-knowledge-base
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

Notes: |
  This task registers source documents only. Chunking, embedding, and vector indexing are T13.

## T09: Cohorts And Enrollment

Owner:      codex
Phase:      2
Type:       none
Depends-On: T07

Objective: |
  Implement cohort creation, learner enrollment, manager assignment, and deterministic mission assignment generation from a launched role-pack version.

Acceptance-Criteria:
  - id: AC-1
    description: "POST /cohorts creates a cohort with role_pack_version, manager_id, start_date, due_date, and status=draft."
    test: "tests/integration/test_cohorts.py::test_create_draft_cohort"
  - id: AC-2
    description: "Launching a cohort creates one mission assignment per active mission for each enrolled learner."
    test: "tests/integration/test_cohorts.py::test_launch_creates_assignments_for_each_learner"
  - id: AC-3
    description: "A learner not enrolled in a cohort receives HTTP 403 when requesting that cohort's assignments."
    test: "tests/integration/test_cohorts.py::test_unenrolled_learner_cannot_read_assignments"

Files:
  - ai_rollout_os/training/cohort_models.py
  - ai_rollout_os/training/cohort_routes.py
  - ai_rollout_os/training/cohort_service.py
  - migrations/versions/0004_cohorts.py
  - tests/integration/test_cohorts.py

Context-Refs:
  - docs/spec.md#feature-cohorts-and-enrollment
  - docs/ARCHITECTURE.md#human-approval-boundaries

Notes: |
  Assignment generation must be idempotent by cohort ID and role-pack version.

## T10: Guardrail Quiz Engine

Owner:      codex
Phase:      2
Type:       none
Depends-On: T07, T09

Objective: |
  Implement guardrail quiz creation, deterministic scoring, mission gating, and persisted quiz results.

Acceptance-Criteria:
  - id: AC-1
    description: "POST /guardrail-quizzes stores questions, answer choices, correct answer IDs, explanations, and pass threshold."
    test: "tests/integration/test_guardrails.py::test_create_guardrail_quiz"
  - id: AC-2
    description: "Submitting quiz answers returns score, pass boolean, and missed question IDs based only on stored answer keys."
    test: "tests/integration/test_guardrails.py::test_quiz_scoring_is_deterministic"
  - id: AC-3
    description: "A mission requiring a passing quiz blocks feedback release until the learner has a passing quiz_result."
    test: "tests/integration/test_guardrails.py::test_feedback_release_requires_passing_quiz"

Files:
  - ai_rollout_os/training/guardrail_models.py
  - ai_rollout_os/training/guardrail_routes.py
  - ai_rollout_os/training/guardrail_service.py
  - migrations/versions/0005_guardrails.py
  - tests/integration/test_guardrails.py

Context-Refs:
  - docs/spec.md#feature-guardrail-quizzes
  - docs/ARCHITECTURE.md#deterministic-vs-llm-owned-subproblems

Notes: |
  LLMs do not score guardrail quizzes.

## Phase 3 - Submissions, Retrieval, And Feedback

Goal: store learner submissions, protect sensitive text, build text-only retrieval, and produce cited rubric feedback.

## T11: Submission Storage And Review States

Owner:      codex
Phase:      3
Type:       none
Depends-On: T09, T10

Objective: |
  Implement learner text submissions, submission versioning, review state transitions, and policy snapshot capture.

Acceptance-Criteria:
  - id: AC-1
    description: "POST /missions/{mission_id}/submissions stores learner text, assignment ID, policy snapshot ID, rubric ID, and review_state=submitted."
    test: "tests/integration/test_submissions.py::test_create_submission_records_snapshot_and_rubric"
  - id: AC-2
    description: "A second submission for the same assignment creates version=2 while preserving version=1."
    test: "tests/integration/test_submissions.py::test_revision_preserves_submission_history"
  - id: AC-3
    description: "Submission creation writes an audit event with action=submission.created and resource_id set to the submission ID."
    test: "tests/integration/test_submissions.py::test_submission_create_emits_audit_event"

Files:
  - ai_rollout_os/submissions/__init__.py
  - ai_rollout_os/submissions/models.py
  - ai_rollout_os/submissions/routes.py
  - ai_rollout_os/submissions/service.py
  - migrations/versions/0006_submissions.py
  - tests/integration/test_submissions.py

Context-Refs:
  - docs/spec.md#feature-learner-submissions
  - docs/ARCHITECTURE.md#learner-submission-and-feedback

Notes: |
  This task stores submitted text but does not generate feedback.

## T12: Sensitive Data Redaction Gate

Owner:      codex
Phase:      3
Type:       none
Depends-On: T11

Objective: |
  Add deterministic sensitive-data checks for submitted text and document bodies, block risky submissions from feedback generation, and preserve auditable redaction state.

Acceptance-Criteria:
  - id: AC-1
    description: "Submitting text containing an email address or configured customer-data marker sets redaction_status=flagged and review_state=blocked_for_review."
    test: "tests/integration/test_redaction.py::test_sensitive_submission_blocks_feedback"
  - id: AC-2
    description: "Flagged text values are not emitted in logs, span attributes, metrics labels, or client error messages."
    test: "tests/integration/test_redaction.py::test_flagged_text_not_exposed_in_observability"
  - id: AC-3
    description: "A manager can mark a flagged submission as approved_for_feedback with a note and the action writes an audit event."
    test: "tests/integration/test_redaction.py::test_manager_approval_unblocks_with_audit_event"

Files:
  - ai_rollout_os/submissions/redaction.py
  - ai_rollout_os/submissions/service.py
  - ai_rollout_os/submissions/routes.py
  - tests/integration/test_redaction.py

Context-Refs:
  - docs/ARCHITECTURE.md#pii-and-sensitive-data-policy
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

Notes: |
  Start with deterministic patterns and configurable markers. Do not send flagged text to an LLM in this task.

Execution-Mode: heavy
Evidence:
  - tests/integration/test_redaction.py::test_sensitive_submission_blocks_feedback
  - tests/integration/test_redaction.py::test_flagged_text_not_exposed_in_observability
Verifier-Focus: |
  Confirm sensitive text cannot leak through errors, logs, span attributes, or metrics and that feedback generation is blocked until manager approval.

## T13: Text Retrieval Ingestion Pipeline

Owner:      codex
Phase:      3
Type:       rag:ingestion
Depends-On: T08, T12

Objective: |
  Adapt the Dream Motif Interpreter RAG ingestion pattern for text-only policy/SOP documents: document normalization, section-aware chunking, embedding adapter interface, pgvector indexing, corpus version recording, and retrieval evaluation dataset initialization.

Acceptance-Criteria:
  - id: AC-1
    description: "Ingesting a policy document creates chunks with source_id, section_path, snapshot_id, index_schema_version='v1', and vector values."
    test: "tests/integration/test_retrieval_ingestion.py::test_ingestion_creates_versioned_chunks"
  - id: AC-2
    description: "Re-ingesting a changed document creates a new corpus_version and leaves prior chunks queryable by their snapshot ID."
    test: "tests/integration/test_retrieval_ingestion.py::test_reingest_preserves_prior_snapshot"
  - id: AC-3
    description: "docs/retrieval_eval.md contains at least 10 initialized evaluation queries covering simple, multi-doc, multi-hop, and no-answer types."
    test: "tests/test_retrieval_eval_doc.py::test_retrieval_eval_dataset_has_required_coverage"
  - id: AC-4
    description: "The ingestion module does not import the query-time retrieval module, preserving the Dream Motif ingestion/query separation safeguard."
    test: "tests/unit/test_retrieval_ingestion.py::test_ingestion_does_not_import_query_module"
  - id: AC-5
    description: "Chunking uses token-aware 512-token boundaries with overlap, adapted from the Dream Motif tiktoken chunking pattern."
    test: "tests/unit/test_retrieval_ingestion.py::test_chunks_respect_token_boundary_and_overlap"

Files:
  - ai_rollout_os/retrieval/chunking.py
  - ai_rollout_os/retrieval/embeddings.py
  - ai_rollout_os/retrieval/ingestion.py
  - ai_rollout_os/retrieval/vector_repository.py
  - migrations/versions/0007_retrieval_chunks.py
  - docs/retrieval_eval.md
  - docs/reference/dream_motif_rag_reuse.md
  - tests/integration/test_retrieval_ingestion.py
  - tests/unit/test_retrieval_ingestion.py
  - tests/test_retrieval_eval_doc.py

Context-Refs:
  - docs/ARCHITECTURE.md#rag-architecture
  - docs/IMPLEMENTATION_CONTRACT.md#profile-rules-rag
  - docs/retrieval_eval.md#evaluation-dataset
  - docs/reference/dream_motif_rag_reuse.md#source-files-to-study-during-implementation

Notes: |
  Start from the reusable shapes in Dream Motif Interpreter: `app/retrieval/types.py`, `app/retrieval/ingestion.py`, `tests/unit/test_rag_ingestion.py`, `tests/integration/test_rag_ingestion.py`, and pgvector/HNSW migrations. Replace dream models and fields with policy/SOP document snapshots and citation metadata.

Execution-Mode: heavy
Evidence:
  - tests/integration/test_retrieval_ingestion.py::test_ingestion_creates_versioned_chunks
  - tests/test_retrieval_eval_doc.py::test_retrieval_eval_dataset_has_required_coverage
  - tests/unit/test_retrieval_ingestion.py::test_ingestion_does_not_import_query_module
Verifier-Focus: |
  Confirm schema versioning, snapshot preservation, corpus version recording, ingestion/query separation, and removal of all dream-domain models from adapted code.

## T14: Retrieval Query And Evidence Assembly

Owner:      codex
Phase:      3
Type:       rag:query
Depends-On: T13

Objective: |
  Adapt the Dream Motif Interpreter query-time RAG pattern for policy/SOP evidence: hybrid pgvector/FTS retrieval, metadata filtering, evidence assembly, citation formatting, and mandatory `insufficient_evidence` behavior.

Acceptance-Criteria:
  - id: AC-1
    description: "Retrieval queries filter by workspace_id, snapshot_id, document_type, and minimum score before returning evidence blocks."
    test: "tests/integration/test_retrieval_query.py::test_query_filters_by_workspace_snapshot_and_score"
  - id: AC-2
    description: "A query with no chunk above threshold returns status='insufficient_evidence' and no generated policy answer."
    test: "tests/integration/test_retrieval_query.py::test_query_returns_insufficient_evidence_below_threshold"
  - id: AC-3
    description: "Evidence blocks include source_id, section_path, chunk_id, score, and citation snippet for every returned chunk."
    test: "tests/integration/test_retrieval_query.py::test_evidence_blocks_include_required_citation_fields"
  - id: AC-4
    description: "Hybrid retrieval uses both pgvector cosine candidates and PostgreSQL FTS candidates with reciprocal rank fusion."
    test: "tests/unit/test_retrieval_query.py::test_query_uses_vector_fts_and_rrf"
  - id: AC-5
    description: "The query-time retrieval module does not import ingestion code, preserving the Dream Motif query/ingestion separation safeguard."
    test: "tests/unit/test_retrieval_query.py::test_query_does_not_import_ingestion_module"

Files:
  - ai_rollout_os/retrieval/query.py
  - ai_rollout_os/retrieval/evidence.py
  - ai_rollout_os/retrieval/vector_repository.py
  - docs/reference/dream_motif_rag_reuse.md
  - tests/integration/test_retrieval_query.py
  - tests/unit/test_retrieval_query.py

Context-Refs:
  - docs/ARCHITECTURE.md#query-time-pipeline
  - docs/IMPLEMENTATION_CONTRACT.md#insufficient_evidence-path
  - docs/retrieval_eval.md#no-answer-behavior-quality
  - docs/reference/dream_motif_rag_reuse.md#source-files-to-study-during-implementation

Notes: |
  Start from Dream Motif `app/retrieval/query.py`, but remove dream-symbolic query profiles and fragment logic. Evidence assembly is deterministic and citation fields are not invented by the LLM.

Execution-Mode: heavy
Evidence:
  - tests/integration/test_retrieval_query.py::test_query_returns_insufficient_evidence_below_threshold
  - tests/integration/test_retrieval_query.py::test_evidence_blocks_include_required_citation_fields
  - tests/unit/test_retrieval_query.py::test_query_uses_vector_fts_and_rrf
Verifier-Focus: |
  Confirm no-answer behavior, source traceability, hybrid retrieval, workspace/snapshot filtering, and removal of all dream-domain query expansion behavior.

## T15: Rubric Evaluation Engine

Owner:      codex
Phase:      3
Type:       none
Depends-On: T10, T11, T14

Objective: |
  Implement structured rubric evaluation that combines deterministic mission state, guardrail results, retrieved evidence, and validated LLM feedback output.

Acceptance-Criteria:
  - id: AC-1
    description: "The feedback schema requires rubric_outcome, learner_feedback, manager_notes, citations, risk_flags, and validation_status."
    test: "tests/unit/test_feedback_schema.py::test_feedback_schema_requires_expected_fields"
  - id: AC-2
    description: "Feedback generation rejects LLM output that contains a citation ID absent from assembled evidence."
    test: "tests/unit/test_feedback_validation.py::test_feedback_rejects_unknown_citation_id"
  - id: AC-3
    description: "When retrieval status is insufficient_evidence, the evaluation engine stores feedback_status=needs_human_review without learner-facing policy guidance."
    test: "tests/integration/test_feedback_engine.py::test_insufficient_evidence_routes_to_human_review"

Files:
  - ai_rollout_os/feedback/__init__.py
  - ai_rollout_os/feedback/schemas.py
  - ai_rollout_os/feedback/engine.py
  - ai_rollout_os/feedback/repository.py
  - tests/unit/test_feedback_schema.py
  - tests/unit/test_feedback_validation.py
  - tests/integration/test_feedback_engine.py

Context-Refs:
  - docs/ARCHITECTURE.md#inference-model-strategy
  - docs/spec.md#feature-ai-assisted-rubric-feedback

Notes: |
  The engine may prepare prompts and validate structured output, but it does not approve workflow changes.

## Phase 4 - Review, Dashboard, And Reports

Goal: run background feedback jobs, manager approvals, deterministic dashboards, exports, and role-pack iteration workflows.

## T16: Feedback Background Jobs

Owner:      codex
Phase:      4
Type:       none
Depends-On: T15

Objective: |
  Implement a PostgreSQL-backed job table and worker process for retryable feedback generation with idempotency keys and timeout handling.

Acceptance-Criteria:
  - id: AC-1
    description: "Creating a ready_for_feedback submission enqueues exactly one feedback job keyed by submission_id and submission_version."
    test: "tests/integration/test_feedback_jobs.py::test_submission_enqueues_one_feedback_job"
  - id: AC-2
    description: "Retrying the same feedback job after a transient LLM error updates the existing job attempt count and does not create duplicate feedback rows."
    test: "tests/integration/test_feedback_jobs.py::test_retry_does_not_duplicate_feedback"
  - id: AC-3
    description: "A job exceeding FEEDBACK_TIMEOUT_SECONDS stores status=timed_out and leaves submission review_state=needs_human_review."
    test: "tests/integration/test_feedback_jobs.py::test_timeout_routes_submission_to_review"

Files:
  - ai_rollout_os/jobs/__init__.py
  - ai_rollout_os/jobs/models.py
  - ai_rollout_os/jobs/worker.py
  - ai_rollout_os/feedback/jobs.py
  - migrations/versions/0008_jobs.py
  - tests/integration/test_feedback_jobs.py

Context-Refs:
  - docs/ARCHITECTURE.md#runtime-and-isolation-model
  - docs/IMPLEMENTATION_CONTRACT.md#control-surface-and-runtime-boundaries

Notes: |
  The worker is bounded and deterministic around LLM calls. It is not an agent loop.

## T17: Manager Review And Approval Workflow

Owner:      codex
Phase:      4
Type:       none
Depends-On: T16

Objective: |
  Implement manager queues, approval and rejection state transitions, approval notes, and separation between AI feedback and human-approved workflow changes.

Acceptance-Criteria:
  - id: AC-1
    description: "GET /manager/submissions filters by learner_id, mission_id, feedback_status, guardrail_status, and risk_flag."
    test: "tests/integration/test_manager_review.py::test_manager_submission_filters"
  - id: AC-2
    description: "POST /manager/submissions/{id}/approve stores approval note, manager_id, approved_at, and approved_workflow_change text."
    test: "tests/integration/test_manager_review.py::test_manager_can_approve_workflow_change"
  - id: AC-3
    description: "The feedback job cannot set manager approval fields on a submission."
    test: "tests/integration/test_manager_review.py::test_feedback_job_cannot_set_manager_approval"

Files:
  - ai_rollout_os/submissions/review_routes.py
  - ai_rollout_os/submissions/review_service.py
  - ai_rollout_os/submissions/models.py
  - tests/integration/test_manager_review.py

Context-Refs:
  - docs/spec.md#feature-manager-review-and-approvals
  - docs/ARCHITECTURE.md#human-approval-boundaries

Notes: |
  Manager approval is the core adoption evidence for v1. Keep it separate from feedback rows.

## T18: Dashboard Metrics

Owner:      codex
Phase:      4
Type:       none
Depends-On: T17

Objective: |
  Implement deterministic cohort metrics and manager dashboard API responses backed by stored records.

Acceptance-Criteria:
  - id: AC-1
    description: "GET /manager/cohorts/{id}/dashboard returns completion_rate, submission_rate, guardrail_pass_rate, approved_workflow_count, feedback_backlog, and sensitive_data_flag_rate."
    test: "tests/integration/test_dashboard.py::test_dashboard_returns_required_metrics"
  - id: AC-2
    description: "Dashboard metric values are computed from database records and do not call the LLM provider."
    test: "tests/integration/test_dashboard.py::test_dashboard_does_not_call_llm_provider"
  - id: AC-3
    description: "Empty cohorts return zero-valued metrics with denominator fields set to zero."
    test: "tests/integration/test_dashboard.py::test_empty_cohort_dashboard_has_zero_metrics"

Files:
  - ai_rollout_os/reporting/__init__.py
  - ai_rollout_os/reporting/dashboard.py
  - ai_rollout_os/reporting/routes.py
  - tests/integration/test_dashboard.py

Context-Refs:
  - docs/spec.md#feature-dashboard-and-reports
  - docs/ARCHITECTURE.md#deterministic-vs-llm-owned-subproblems

Notes: |
  Narrative summaries are separate from deterministic metrics and are not part of this task.

## T19: Exportable Progress Reports

Owner:      codex
Phase:      4
Type:       none
Depends-On: T18

Objective: |
  Generate versioned Markdown and JSON progress reports containing cohort metadata, metrics, approved workflow changes, risks, and policy snapshot references.

Acceptance-Criteria:
  - id: AC-1
    description: "POST /manager/cohorts/{id}/reports creates a report version containing cohort metadata, role-pack version, policy snapshot ID, and dashboard metrics."
    test: "tests/integration/test_reports.py::test_create_report_version_with_required_metadata"
  - id: AC-2
    description: "Generated Markdown report includes approved workflow changes and open risk flags without learner submission body text."
    test: "tests/integration/test_reports.py::test_markdown_report_excludes_submission_body_text"
  - id: AC-3
    description: "Report generation writes an audit event with action=report.created and resource_id set to the report ID."
    test: "tests/integration/test_reports.py::test_report_generation_emits_audit_event"

Files:
  - ai_rollout_os/reporting/reports.py
  - ai_rollout_os/reporting/report_routes.py
  - migrations/versions/0009_reports.py
  - tests/integration/test_reports.py

Context-Refs:
  - docs/spec.md#feature-dashboard-and-reports
  - docs/EVIDENCE_INDEX.md#evidence-table

Notes: |
  Reports summarize evidence and link to records. They do not expose raw sensitive artifacts.

## T20: Role Pack Version Iteration

Owner:      codex
Phase:      4
Type:       none
Depends-On: T17, T19

Objective: |
  Let operators revise role packs, rubrics, guardrail questions, and mission templates after reviewing cohort failures while preserving historical versions.

Acceptance-Criteria:
  - id: AC-1
    description: "Updating a launched role pack creates version N+1 and leaves existing cohort assignments linked to their original version."
    test: "tests/integration/test_role_pack_versions.py::test_launched_role_pack_update_creates_new_version"
  - id: AC-2
    description: "A version comparison response lists changed missions, changed rubric IDs, changed guardrail quiz IDs, and unchanged missions."
    test: "tests/integration/test_role_pack_versions.py::test_role_pack_version_diff_lists_changes"
  - id: AC-3
    description: "Operator edits write audit events with previous_version and new_version metadata."
    test: "tests/integration/test_role_pack_versions.py::test_role_pack_version_edit_audited"

Files:
  - ai_rollout_os/training/versioning.py
  - ai_rollout_os/training/routes.py
  - ai_rollout_os/training/service.py
  - tests/integration/test_role_pack_versions.py

Context-Refs:
  - docs/ARCHITECTURE.md#runtime-and-isolation-model
  - docs/IMPLEMENTATION_JOURNAL.md#entries

Notes: |
  Versioning is required for auditability and future agent continuity.

## Phase 5 - Pilot Readiness

Goal: add reminders, retrieval evaluation automation, deployment assets, and a pilot readiness gate.

## T21: Reminder Scheduler

Owner:      codex
Phase:      5
Type:       none
Depends-On: T16, T18

Objective: |
  Implement deterministic reminder jobs for due missions, manager review backlog, and stale feedback jobs with optional Slack or Telegram delivery adapters disabled by default.

Acceptance-Criteria:
  - id: AC-1
    description: "The scheduler creates reminder jobs for assignments due within the configured reminder window."
    test: "tests/integration/test_reminders.py::test_scheduler_creates_due_assignment_reminders"
  - id: AC-2
    description: "Running the scheduler twice for the same due assignment produces one reminder record keyed by assignment_id and reminder_type."
    test: "tests/integration/test_reminders.py::test_scheduler_is_idempotent_per_assignment"
  - id: AC-3
    description: "When external reminder delivery is disabled, reminder jobs are stored with status=queued_without_delivery and no external API call is made."
    test: "tests/integration/test_reminders.py::test_disabled_delivery_makes_no_external_call"

Files:
  - ai_rollout_os/jobs/reminders.py
  - ai_rollout_os/jobs/delivery.py
  - migrations/versions/0010_reminders.py
  - tests/integration/test_reminders.py

Context-Refs:
  - docs/ARCHITECTURE.md#external-integrations
  - docs/IMPLEMENTATION_CONTRACT.md#control-surface-and-runtime-boundaries

Notes: |
  External messaging is not LLM-directed tool use. Any MCP-backed reminder integration requires ADR.

## T22: Retrieval Evaluation Automation

Owner:      codex
Phase:      5
Type:       rag:query
Depends-On: T13, T14

Objective: |
  Adapt the Dream Motif Interpreter retrieval evaluation script and tests for AI Rollout Training OS policy/SOP retrieval: hit@3, hit@5, MRR, citation precision, no-answer accuracy, citation-field presence, and retrieval latency against docs/retrieval_eval.md.

Acceptance-Criteria:
  - id: AC-1
    description: "scripts/eval.py computes hit@3, hit@5, MRR, citation precision, no-answer accuracy, median retrieval latency, and p95 retrieval latency from the retrieval evaluation dataset."
    test: "tests/eval/test_retrieval_eval.py::test_retrieval_quality_metrics_meet_baseline"
  - id: AC-2
    description: "The evaluation test fails when a no-answer query returns generated guidance instead of insufficient_evidence."
    test: "tests/eval/test_retrieval_eval.py::test_no_answer_queries_require_insufficient_evidence"
  - id: AC-3
    description: "docs/retrieval_eval.md Evaluation History contains a row for the automated run with Eval Source, Date, and Corpus Version."
    test: "tests/test_retrieval_eval_doc.py::test_evaluation_history_rows_have_required_fields"
  - id: AC-4
    description: "scripts/eval.py supports a no-write mode that runs metrics without modifying docs/retrieval_eval.md."
    test: "tests/unit/test_eval_script.py::test_main_passes_no_write_markdown_flag_to_run_evaluation"
  - id: AC-5
    description: "The evaluation path uses deterministic stub embeddings when provider keys are absent or test-prefixed."
    test: "tests/unit/test_eval_script.py::test_eval_uses_stub_embeddings_for_test_keys"

Files:
  - scripts/eval.py
  - tests/fixtures/seed_training_documents.json
  - tests/eval/test_retrieval_eval.py
  - tests/unit/test_eval_script.py
  - tests/test_retrieval_eval_doc.py
  - docs/retrieval_eval.md
  - docs/reference/dream_motif_rag_reuse.md
  - .github/workflows/ci.yml

Context-Refs:
  - docs/retrieval_eval.md#evaluation-validity-rule
  - docs/IMPLEMENTATION_CONTRACT.md#retrieval-evaluation-gate
  - docs/reference/dream_motif_rag_reuse.md#source-files-to-study-during-implementation

Notes: |
  Adapt Dream Motif `scripts/eval.py`, `tests/unit/test_eval_script.py`, `tests/unit/test_retrieval_eval.py`, and `tests/integration/test_retrieval_eval.py`. Replace seed dreams with policy/SOP/role-pack fixture documents that match this project's eval dataset. Keep CI-safe stub embeddings.

## T23: Docker Compose Deployment

Owner:      codex
Phase:      5
Type:       none
Depends-On: T22

Objective: |
  Add Dockerfile, Docker Compose, migration command, app service, worker service, and PostgreSQL/pgvector service for early VPS pilots.

Acceptance-Criteria:
  - id: AC-1
    description: "docker compose config validates web, worker, and postgres services with required environment variable names."
    test: "tests/test_deployment_files.py::test_docker_compose_config_contains_required_services"
  - id: AC-2
    description: "The worker service starts from the same image as the web service and runs the bounded feedback/reminder worker command."
    test: "tests/test_deployment_files.py::test_worker_uses_same_image_and_bounded_command"
  - id: AC-3
    description: "Deployment files contain no real secret values and refer to .env.example placeholders."
    test: "tests/test_deployment_files.py::test_deployment_files_have_no_real_secrets"

Files:
  - Dockerfile
  - docker-compose.yml
  - .env.example
  - tests/test_deployment_files.py

Context-Refs:
  - docs/ARCHITECTURE.md#runtime-and-isolation-model
  - docs/IMPLEMENTATION_CONTRACT.md#credentials-and-secrets

Notes: |
  Stay within T1. Do not add runtime shell mutation or privileged container permissions.

## T24: Pilot Readiness Gate

Owner:      codex
Phase:      5
Type:       none
Depends-On: T19, T20, T21, T22, T23

Objective: |
  Add a pilot readiness checklist, seed data for one role pack, and tests proving the core pilot path can run from cohort launch through report export.

Acceptance-Criteria:
  - id: AC-1
    description: "The pilot fixture creates one operator, one manager, two learners, one role pack, two missions, one guardrail quiz, and policy/SOP documents."
    test: "tests/integration/test_pilot_readiness.py::test_pilot_fixture_creates_minimum_dataset"
  - id: AC-2
    description: "The end-to-end pilot test launches a cohort, submits one artifact, generates feedback, records manager approval, and creates a report."
    test: "tests/integration/test_pilot_readiness.py::test_end_to_end_pilot_flow"
  - id: AC-3
    description: "docs/pilot_readiness.md lists required env vars, operator setup steps, known non-goals, and go/no-go checks for the first pilot."
    test: "tests/test_pilot_readiness_doc.py::test_pilot_readiness_doc_contains_required_sections"

Files:
  - docs/pilot_readiness.md
  - tests/fixtures/pilot_data.py
  - tests/integration/test_pilot_readiness.py
  - tests/test_pilot_readiness_doc.py

Context-Refs:
  - docs/ARCHITECTURE.md#problem-fit-and-adoption-reality
  - docs/spec.md#overview
  - docs/EVIDENCE_INDEX.md#evidence-table

Notes: |
  This is the v1 pilot gate, not a production certification gate.
