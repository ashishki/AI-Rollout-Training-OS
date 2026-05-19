# Product Maturity Task Graph

Version: 1.0
Last updated: 2026-05-19
Scope: post-MVP production maturity, starting after T24.

This file extends `docs/tasks.md`. The Codex-only loop should select tasks from
this file when `docs/CODEX_PROMPT.md` points to T25 or later.

---

## Phase 6 - PMF Pilot System

Goal: prove a narrow market wedge and instrument measurable pilot outcomes.

## T25: Pilot Outcome Metrics Model

Owner:      codex
Phase:      6
Type:       product+analytics
Depends-On: T24

Objective: |
  Define and implement pilot outcome metrics: activation, completion, approved
  workflow changes, manager review time, risk rate, and time-to-first-safe-use.

Acceptance-Criteria:
  - id: AC-1
    description: "A pilot metrics service computes required outcome metrics from stored records without LLM-generated values."
    test: "tests/integration/test_pilot_metrics.py::test_pilot_metrics_are_database_derived"
  - id: AC-2
    description: "docs/product_maturity_roadmap.md lists the Phase 6 metrics and exit gate."
    test: "tests/test_product_maturity_docs.py::test_roadmap_lists_phase_6_metrics"

Files:
  - ai_rollout_os/reporting/pilot_metrics.py
  - tests/integration/test_pilot_metrics.py
  - docs/product_maturity_roadmap.md

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-6---pmf-pilot-system
  - docs/IMPLEMENTATION_CONTRACT.md#deterministic-metrics

## T26: Customer Discovery Evidence Registry

Owner:      codex
Phase:      6
Type:       product
Depends-On: T25

Objective: |
  Add a structured discovery registry for ICP, buyer, blocker, workaround,
  willingness-to-pay signal, pilot outcome notes, and confidence level.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/customer_discovery.md contains evidence schema, interview log template, and decision rules."
    test: "tests/test_customer_discovery_doc.py::test_customer_discovery_doc_has_required_sections"
  - id: AC-2
    description: "The registry distinguishes observed customer evidence from internal assumptions."
    test: "tests/test_customer_discovery_doc.py::test_customer_discovery_doc_distinguishes_evidence_from_assumptions"

Files:
  - docs/customer_discovery.md
  - tests/test_customer_discovery_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#target-market-wedge

## T27: Pilot Success Rubric

Owner:      codex
Phase:      6
Type:       product
Depends-On: T25, T26

Objective: |
  Create a go/no-go rubric for whether a pilot should expand, repeat, pause,
  or reposition.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/pilot_success_rubric.md defines expansion, repeat, pause, and reposition outcomes."
    test: "tests/test_pilot_success_rubric.py::test_success_rubric_has_outcome_decisions"
  - id: AC-2
    description: "The rubric includes product, quality, and business metrics."
    test: "tests/test_pilot_success_rubric.py::test_success_rubric_covers_metric_groups"

Files:
  - docs/pilot_success_rubric.md
  - tests/test_pilot_success_rubric.py

Context-Refs:
  - docs/product_maturity_roadmap.md#metrics-that-matter

## T28: Pilot ROI Report

Owner:      codex
Phase:      6
Type:       reporting
Depends-On: T25, T27

Objective: |
  Add a conservative pilot ROI report that summarizes adoption, approved
  workflow changes, risk reduction signals, and manual review savings without
  claiming guaranteed productivity gains.

Acceptance-Criteria:
  - id: AC-1
    description: "The ROI report excludes productivity guarantees and labels assumptions explicitly."
    test: "tests/integration/test_pilot_roi_report.py::test_roi_report_avoids_productivity_claims"
  - id: AC-2
    description: "The ROI report includes metric source and denominator fields."
    test: "tests/integration/test_pilot_roi_report.py::test_roi_report_includes_metric_denominators"

Files:
  - ai_rollout_os/reporting/pilot_roi.py
  - tests/integration/test_pilot_roi_report.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries
  - docs/product_maturity_roadmap.md#metrics-that-matter

## T29: Phase 6 PMF Gate

Owner:      codex
Phase:      6
Type:       audit
Depends-On: T25, T26, T27, T28

Objective: |
  Add the Phase 6 review gate and decide whether PMF evidence supports moving
  into core product UX work.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/audit/PHASE6_PMF_AUDIT.md records PMF evidence, gaps, and go/no-go status."
    test: "tests/test_phase6_audit_doc.py::test_phase6_audit_records_pmf_gate"

Files:
  - docs/audit/PHASE6_PMF_AUDIT.md
  - docs/audit/AUDIT_INDEX.md
  - tests/test_phase6_audit_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-6---pmf-pilot-system

## Phase 7 - Core Product UX

Goal: make the pilot flow operable by non-engineers.

## T30: Frontend Application Shell

Owner:      codex
Phase:      7
Type:       frontend
Depends-On: T29

Objective: |
  Add the frontend shell with authenticated operator, manager, and learner
  navigation surfaces.

Acceptance-Criteria:
  - id: AC-1
    description: "The app shell exposes role-specific navigation without landing-page detours."
    test: "tests/e2e/test_app_shell.py::test_role_navigation_shell"
  - id: AC-2
    description: "Protected views require authentication."
    test: "tests/e2e/test_app_shell.py::test_protected_views_require_auth"

Files:
  - frontend/
  - tests/e2e/test_app_shell.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-7---core-product-ux

## T31: Operator Admin UI

Owner:      codex
Phase:      7
Type:       frontend
Depends-On: T30

Objective: |
  Build operator UI for policies, role packs, missions, guardrail quizzes,
  cohorts, and launches.

Acceptance-Criteria:
  - id: AC-1
    description: "An operator can create and launch a role pack and cohort through the UI."
    test: "tests/e2e/test_operator_admin.py::test_operator_launches_cohort"
  - id: AC-2
    description: "Policy/SOP body text is never shown in logs or client error text."
    test: "tests/e2e/test_operator_admin.py::test_policy_errors_do_not_leak_body_text"

Files:
  - frontend/
  - tests/e2e/test_operator_admin.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

## T32: Learner Mission UI

Owner:      codex
Phase:      7
Type:       frontend
Depends-On: T30

Objective: |
  Build learner UI for assignments, guardrail quizzes, submissions, feedback
  status, and feedback review.

Acceptance-Criteria:
  - id: AC-1
    description: "A learner can complete a quiz and submit an artifact through the UI."
    test: "tests/e2e/test_learner_missions.py::test_learner_completes_mission_flow"
  - id: AC-2
    description: "Flagged sensitive submissions display redacted text only."
    test: "tests/e2e/test_learner_missions.py::test_flagged_submission_is_redacted"

Files:
  - frontend/
  - tests/e2e/test_learner_missions.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#artifact-retention-and-redaction

## T33: Manager Review UI

Owner:      codex
Phase:      7
Type:       frontend
Depends-On: T30

Objective: |
  Build manager queue, filters, approval, dashboard, and report views.

Acceptance-Criteria:
  - id: AC-1
    description: "A manager can filter submissions, approve a workflow change, and create a report."
    test: "tests/e2e/test_manager_review.py::test_manager_approval_and_report_flow"
  - id: AC-2
    description: "Manager notes are not logged or included in metric labels."
    test: "tests/e2e/test_manager_review.py::test_manager_notes_not_logged"

Files:
  - frontend/
  - tests/e2e/test_manager_review.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries

## T34: UX Readiness Gate

Owner:      codex
Phase:      7
Type:       audit
Depends-On: T30, T31, T32, T33

Objective: |
  Add the Phase 7 UX readiness audit for non-engineer pilot operation.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/audit/PHASE7_UX_AUDIT.md records critical workflows and open UX blockers."
    test: "tests/test_phase7_audit_doc.py::test_phase7_audit_records_workflow_status"

Files:
  - docs/audit/PHASE7_UX_AUDIT.md
  - docs/audit/AUDIT_INDEX.md
  - tests/test_phase7_audit_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-7---core-product-ux

## Phase 8 - Enterprise Security

Goal: pass credible IT/security review for real deployments.

## T35: SSO And Identity Boundary

Owner:      codex
Phase:      8
Type:       security
Depends-On: T34

Objective: |
  Add OIDC-based SSO support and document the SAML decision path for later
  enterprise deployments.

Acceptance-Criteria:
  - id: AC-1
    description: "OIDC login maps external users to workspace roles without trusting client-provided roles."
    test: "tests/integration/test_sso.py::test_oidc_login_maps_roles_server_side"
  - id: AC-2
    description: "SSO configuration secrets are environment-only and never committed."
    test: "tests/test_sso_config.py::test_sso_secrets_are_env_only"

Files:
  - ai_rollout_os/auth/sso.py
  - tests/integration/test_sso.py
  - docs/security_review.md

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#credentials-and-secrets

## T36: RBAC Permissions Matrix

Owner:      codex
Phase:      8
Type:       security
Depends-On: T35

Objective: |
  Replace route-level role checks with a documented permission matrix and shared
  enforcement helper.

Acceptance-Criteria:
  - id: AC-1
    description: "Every protected route maps to a named permission."
    test: "tests/test_permissions_matrix.py::test_every_route_has_permission"
  - id: AC-2
    description: "Denied permission checks write audit events."
    test: "tests/integration/test_permissions_matrix.py::test_denied_permission_is_audited"

Files:
  - ai_rollout_os/auth/permissions.py
  - docs/security_review.md
  - tests/test_permissions_matrix.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#authorization

## T37: Backup Restore And Retention

Owner:      codex
Phase:      8
Type:       ops
Depends-On: T36

Objective: |
  Add documented backup/restore procedures and retention controls for pilot
  deployments.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/backup_restore.md defines backup, restore, retention, and rollback steps."
    test: "tests/test_backup_restore_doc.py::test_backup_restore_doc_has_required_sections"
  - id: AC-2
    description: "Retention jobs redact/delete mutable artifact data without deleting audit events."
    test: "tests/integration/test_retention.py::test_retention_preserves_audit_events"

Files:
  - ai_rollout_os/jobs/retention.py
  - docs/backup_restore.md
  - tests/integration/test_retention.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#artifact-retention-and-redaction

## T38: Security Review Packet

Owner:      codex
Phase:      8
Type:       security
Depends-On: T35, T36, T37

Objective: |
  Produce the first enterprise security review packet covering architecture,
  data flows, subprocessors, secrets, audit logs, and incident response.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/security_review.md contains architecture, data flow, subprocessors, controls, and incident response sections."
    test: "tests/test_security_review_doc.py::test_security_review_packet_complete"

Files:
  - docs/security_review.md
  - tests/test_security_review_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-8---enterprise-security

## Phase 9 - Governance Layer

Goal: make the product trustworthy for legal, compliance, and AI governance.

## T39: Policy Approval Workflow

Owner:      codex
Phase:      9
Type:       governance
Depends-On: T38

Objective: |
  Add human-owned approval states for policy and SOP document versions before
  they become active retrieval sources.

Acceptance-Criteria:
  - id: AC-1
    description: "Only approved document snapshots are eligible for active feedback retrieval."
    test: "tests/integration/test_policy_approval.py::test_unapproved_policy_not_retrieved"
  - id: AC-2
    description: "AI paths cannot approve policy versions."
    test: "tests/integration/test_policy_approval.py::test_policy_approval_is_human_owned"

Files:
  - ai_rollout_os/retrieval/document_approval.py
  - migrations/versions/
  - tests/integration/test_policy_approval.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries

## T40: Governance Risk Taxonomy

Owner:      codex
Phase:      9
Type:       governance
Depends-On: T39

Objective: |
  Add a durable risk taxonomy for PII, legal, medical, financial, customer data,
  unsupported claims, and policy ownership.

Acceptance-Criteria:
  - id: AC-1
    description: "Risk flags are normalized against a versioned taxonomy."
    test: "tests/integration/test_risk_taxonomy.py::test_risk_flags_use_taxonomy"
  - id: AC-2
    description: "Unknown risk flags are rejected before manager-facing reports."
    test: "tests/integration/test_risk_taxonomy.py::test_unknown_risk_flag_rejected"

Files:
  - ai_rollout_os/governance/risk_taxonomy.py
  - tests/integration/test_risk_taxonomy.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-9---governance-layer

## T41: Control Mapping And Evidence Lineage

Owner:      codex
Phase:      9
Type:       governance
Depends-On: T39, T40

Objective: |
  Map product evidence to governance controls and expose lineage from source
  document to feedback to approval to report.

Acceptance-Criteria:
  - id: AC-1
    description: "Control mapping export links controls to source documents, submissions, feedback, approvals, and reports."
    test: "tests/integration/test_control_mapping.py::test_control_mapping_export_has_lineage"
  - id: AC-2
    description: "Lineage export contains no raw learner artifact text."
    test: "tests/integration/test_control_mapping.py::test_lineage_export_excludes_raw_artifacts"

Files:
  - ai_rollout_os/governance/controls.py
  - tests/integration/test_control_mapping.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

## T42: Audit Export Package

Owner:      codex
Phase:      9
Type:       governance
Depends-On: T41

Objective: |
  Add a reproducible governance audit export package for a cohort or date range.

Acceptance-Criteria:
  - id: AC-1
    description: "Audit export includes metadata, controls, lineage, approvals, reports, and hashes."
    test: "tests/integration/test_audit_export.py::test_audit_export_package_complete"
  - id: AC-2
    description: "Two exports over unchanged data produce matching hashes."
    test: "tests/integration/test_audit_export.py::test_audit_export_is_reproducible"

Files:
  - ai_rollout_os/governance/audit_export.py
  - tests/integration/test_audit_export.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-9---governance-layer

## Phase 10 - Integrations

Goal: reduce duplicate administration and fit into customer systems.

## T43: Slack And Teams Reminder Adapters

Owner:      codex
Phase:      10
Type:       integration
Depends-On: T21, T38

Objective: |
  Add explicitly enabled Slack and Teams reminder adapters with idempotent
  delivery and safe failure handling.

Acceptance-Criteria:
  - id: AC-1
    description: "Adapters are disabled by default and require explicit env configuration."
    test: "tests/integration/test_reminder_integrations.py::test_reminder_adapters_disabled_by_default"
  - id: AC-2
    description: "Delivery failures keep reminder jobs durable and retryable without duplicate external sends."
    test: "tests/integration/test_reminder_integrations.py::test_reminder_delivery_failure_is_retryable"

Files:
  - ai_rollout_os/jobs/delivery.py
  - tests/integration/test_reminder_integrations.py

Context-Refs:
  - docs/ARCHITECTURE.md#external-integrations

## T44: HRIS User Import

Owner:      codex
Phase:      10
Type:       integration
Depends-On: T36

Objective: |
  Add a safe CSV-first HRIS import path for users, roles, managers, and teams.

Acceptance-Criteria:
  - id: AC-1
    description: "CSV import validates users and roles before mutation."
    test: "tests/integration/test_user_import.py::test_user_import_validates_before_mutation"
  - id: AC-2
    description: "Import errors do not log email addresses or names."
    test: "tests/integration/test_user_import.py::test_user_import_errors_redact_pii"

Files:
  - ai_rollout_os/integrations/user_import.py
  - tests/integration/test_user_import.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

## T45: LMS Completion Export

Owner:      codex
Phase:      10
Type:       integration
Depends-On: T25, T44

Objective: |
  Add a completion export for LMS ingestion with learner IDs, assignment status,
  completion dates, and no raw submission text.

Acceptance-Criteria:
  - id: AC-1
    description: "LMS export includes completion evidence and excludes raw artifacts."
    test: "tests/integration/test_lms_export.py::test_lms_export_excludes_artifacts"

Files:
  - ai_rollout_os/integrations/lms_export.py
  - tests/integration/test_lms_export.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

## T46: Knowledge Base Import V2

Owner:      codex
Phase:      10
Type:       retrieval
Depends-On: T39

Objective: |
  Add a provider-neutral import interface for Google Drive, Confluence, Notion,
  SharePoint, and manual upload v2 while preserving approval and snapshot rules.

Acceptance-Criteria:
  - id: AC-1
    description: "Imported documents are stored as unapproved snapshots until human approval."
    test: "tests/integration/test_knowledge_import.py::test_imported_docs_require_approval"
  - id: AC-2
    description: "Provider failures do not create partial active snapshots."
    test: "tests/integration/test_knowledge_import.py::test_import_failure_does_not_activate_partial_snapshot"

Files:
  - ai_rollout_os/integrations/knowledge_import.py
  - tests/integration/test_knowledge_import.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#profile-rules-rag

## Phase 11 - AI Quality And Model Ops

Goal: make feedback and retrieval quality regression-safe.

## T47: Prompt And Model Registry

Owner:      codex
Phase:      11
Type:       ai-quality
Depends-On: T42

Objective: |
  Add durable prompt, model, rubric, retrieval corpus, and feedback schema
  version registry records.

Acceptance-Criteria:
  - id: AC-1
    description: "Feedback results reference prompt, model, rubric, and corpus versions."
    test: "tests/integration/test_model_registry.py::test_feedback_result_records_versions"

Files:
  - ai_rollout_os/feedback/model_registry.py
  - migrations/versions/
  - tests/integration/test_model_registry.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-11---ai-quality--model-ops

## T48: Feedback Quality Eval Runner

Owner:      codex
Phase:      11
Type:       rag:query
Depends-On: T22, T47

Objective: |
  Add answer-quality evaluation for faithfulness, completeness, relevance, and
  human-review routing across role/customer datasets.

Acceptance-Criteria:
  - id: AC-1
    description: "Feedback eval computes faithfulness, completeness, relevance, and unsupported-claim rate."
    test: "tests/eval/test_feedback_quality_eval.py::test_feedback_quality_metrics"
  - id: AC-2
    description: "Eval history records Eval Source, Date, Corpus Version, Prompt Version, and Model Version."
    test: "tests/test_retrieval_eval_doc.py::test_feedback_eval_history_has_required_fields"

Files:
  - scripts/eval_feedback.py
  - docs/retrieval_eval.md
  - tests/eval/test_feedback_quality_eval.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#retrieval-evaluation-gate

## T49: Human Sampling And Adjudication

Owner:      codex
Phase:      11
Type:       ai-quality
Depends-On: T48

Objective: |
  Add human sampling queues for feedback review and adjudication labels.

Acceptance-Criteria:
  - id: AC-1
    description: "Sampling creates review items without exposing raw artifacts beyond authorized reviewers."
    test: "tests/integration/test_feedback_sampling.py::test_sampling_respects_authorization"
  - id: AC-2
    description: "Adjudication labels update eval datasets without overwriting original feedback."
    test: "tests/integration/test_feedback_sampling.py::test_adjudication_preserves_original_feedback"

Files:
  - ai_rollout_os/feedback/sampling.py
  - tests/integration/test_feedback_sampling.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#authorization

## T50: Cost And Latency Monitoring

Owner:      codex
Phase:      11
Type:       observability
Depends-On: T47

Objective: |
  Add per-provider, per-model, and per-feature cost/latency accounting with
  no sensitive prompt or artifact content in metric labels.

Acceptance-Criteria:
  - id: AC-1
    description: "Cost and latency metrics are tagged by opaque IDs and model names only."
    test: "tests/unit/test_ai_metrics.py::test_ai_metrics_exclude_sensitive_text"

Files:
  - ai_rollout_os/observability/ai_metrics.py
  - tests/unit/test_ai_metrics.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#pii-policy

## Phase 12 - Reliability And Scale

Goal: run safely for many cohorts and teams.

## T51: Service SLO Dashboard

Owner:      codex
Phase:      12
Type:       reliability
Depends-On: T50

Objective: |
  Define SLOs and expose service health metrics for API latency, job latency,
  retrieval latency, error rate, and queue depth.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/slo.md defines SLOs, burn-rate signals, and escalation rules."
    test: "tests/test_slo_doc.py::test_slo_doc_has_required_sections"

Files:
  - docs/slo.md
  - tests/test_slo_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-12---reliability--scale

## T52: Load Test Harness

Owner:      codex
Phase:      12
Type:       reliability
Depends-On: T51

Objective: |
  Add load tests for cohort launch, retrieval, feedback jobs, reminders, and
  report generation.

Acceptance-Criteria:
  - id: AC-1
    description: "Load test script runs with synthetic data and writes p95/p99 latency output."
    test: "tests/test_load_test_harness.py::test_load_test_script_exists_and_reports_required_metrics"

Files:
  - scripts/load_test.py
  - tests/test_load_test_harness.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-12---reliability--scale

## T53: Incident Response Runbook

Owner:      codex
Phase:      12
Type:       reliability
Depends-On: T51

Objective: |
  Add incident response runbooks for retrieval outage, feedback job backlog,
  data leak suspicion, failed migrations, and provider degradation.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/incident_response.md covers required incident classes and escalation steps."
    test: "tests/test_incident_response_doc.py::test_incident_response_doc_complete"

Files:
  - docs/incident_response.md
  - tests/test_incident_response_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-12---reliability--scale

## T54: Migration Rehearsal Gate

Owner:      codex
Phase:      12
Type:       reliability
Depends-On: T37, T52

Objective: |
  Add migration rehearsal checks for upgrade, rollback plan, backup, restore,
  and data validation.

Acceptance-Criteria:
  - id: AC-1
    description: "Migration rehearsal documentation includes upgrade, rollback, backup, restore, and validation steps."
    test: "tests/test_migration_rehearsal_doc.py::test_migration_rehearsal_doc_complete"

Files:
  - docs/migration_rehearsal.md
  - tests/test_migration_rehearsal_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-12---reliability--scale

## Phase 13 - Commercial Packaging

Goal: make the product repeatably sellable and procurable.

## T55: Packaging And Pricing Model

Owner:      codex
Phase:      13
Type:       gtm
Depends-On: T29

Objective: |
  Define Team Pilot, Enterprise Enablement, Governance Plus, and Regulated
  Single-Tenant packages with feature boundaries and pricing drivers.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/packaging.md defines packages, buyer, value metric, and limits."
    test: "tests/test_packaging_doc.py::test_packaging_doc_has_required_tiers"

Files:
  - docs/packaging.md
  - tests/test_packaging_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-13---commercial-packaging

## T56: ROI Calculator

Owner:      codex
Phase:      13
Type:       gtm
Depends-On: T28, T55

Objective: |
  Add a conservative ROI calculator that uses customer-provided assumptions and
  explicitly avoids guaranteed productivity claims.

Acceptance-Criteria:
  - id: AC-1
    description: "ROI calculator labels assumptions and never emits guaranteed productivity claims."
    test: "tests/unit/test_roi_calculator.py::test_roi_calculator_avoids_guarantees"

Files:
  - ai_rollout_os/reporting/roi_calculator.py
  - tests/unit/test_roi_calculator.py

Context-Refs:
  - docs/IMPLEMENTATION_CONTRACT.md#human-approval-boundaries

## T57: Procurement Packet

Owner:      codex
Phase:      13
Type:       gtm
Depends-On: T38, T55

Objective: |
  Assemble procurement materials: security packet, data processing summary,
  deployment options, support model, and implementation plan.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/procurement_packet.md includes security, privacy, deployment, support, and implementation sections."
    test: "tests/test_procurement_packet_doc.py::test_procurement_packet_complete"

Files:
  - docs/procurement_packet.md
  - tests/test_procurement_packet_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-13---commercial-packaging

## T58: Implementation Success Plan

Owner:      codex
Phase:      13
Type:       gtm
Depends-On: T27, T55

Objective: |
  Create a customer-facing implementation plan for kickoff, policy ingestion,
  role-pack setup, cohort launch, manager review, reporting, and expansion.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/implementation_success_plan.md defines kickoff through expansion steps and owner responsibilities."
    test: "tests/test_implementation_success_plan_doc.py::test_implementation_success_plan_complete"

Files:
  - docs/implementation_success_plan.md
  - tests/test_implementation_success_plan_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-13---commercial-packaging

## Phase 14 - GA Readiness

Goal: decide whether the product is ready for general availability.

## T59: GA Readiness Checklist

Owner:      codex
Phase:      14
Type:       audit
Depends-On: T34, T38, T42, T48, T54, T57

Objective: |
  Add the general availability readiness checklist across product, security,
  reliability, AI quality, support, and GTM.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/ga_readiness.md lists required product, security, reliability, AI quality, support, and GTM gates."
    test: "tests/test_ga_readiness_doc.py::test_ga_readiness_doc_complete"

Files:
  - docs/ga_readiness.md
  - tests/test_ga_readiness_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-14---ga-readiness

## T60: Release Notes And Upgrade Guide

Owner:      codex
Phase:      14
Type:       release
Depends-On: T59

Objective: |
  Add release notes and upgrade guide for pilot-to-GA customers.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/release_notes.md and docs/upgrade_guide.md document changes, migrations, rollback, and customer-visible behavior."
    test: "tests/test_release_docs.py::test_release_docs_complete"

Files:
  - docs/release_notes.md
  - docs/upgrade_guide.md
  - tests/test_release_docs.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-14---ga-readiness

## T61: Final Production Readiness Audit

Owner:      codex
Phase:      14
Type:       audit
Depends-On: T59, T60

Objective: |
  Run the final production readiness audit and record open findings, accepted
  risks, and the GA decision.

Acceptance-Criteria:
  - id: AC-1
    description: "docs/audit/PRODUCTION_READINESS_AUDIT.md records GA decision, blockers, accepted risks, and evidence links."
    test: "tests/test_production_readiness_audit_doc.py::test_production_readiness_audit_complete"

Files:
  - docs/audit/PRODUCTION_READINESS_AUDIT.md
  - docs/audit/AUDIT_INDEX.md
  - tests/test_production_readiness_audit_doc.py

Context-Refs:
  - docs/product_maturity_roadmap.md#phase-14---ga-readiness
