# Specification - AI Rollout Training OS

Version: 1.0
Last updated: 2026-05-19

---

## Overview

AI Rollout Training OS helps a company run a measurable AI adoption pilot. Training owners configure role-specific missions, learners submit real workflow artifacts, AI feedback is grounded in company policy and rubrics, managers approve repeatable workflow changes, and rollout operators export adoption evidence.

## User Roles

| Role | Capabilities |
|------|--------------|
| Operator / training owner | Configure role packs, policy documents, cohorts, missions, guardrail quizzes, rubrics, and exports. |
| Learner | View assigned missions, submit text artifacts, answer guardrail questions, receive feedback, and revise submissions. |
| Manager | Review team progress, approve workflow changes, inspect risks, and export reports. |
| System worker | Run background feedback, retrieval ingestion, reminder, and report-generation jobs under deterministic job records. |

## Feature: Role Packs And Missions

### Description

Operators create role packs containing mission templates, rubrics, guardrail questions, and expected workflow artifacts for a specific team role.

### Acceptance Criteria

1. An operator can create a role pack with title, role, mission list, rubric references, and active/inactive status.
2. A mission template stores objective, learner instructions, expected artifact type, guardrail quiz ID, and rubric ID.
3. A role pack cannot be launched when it has zero active missions.
4. Updating a launched role pack creates a new version instead of mutating historical mission records.

### Out Of Scope For v1

- Marketplace role packs.
- Public sharing.
- Automated role-pack publication without operator approval.

## Feature: Company Policy And SOP Knowledge Base

### Description

Operators register company AI policy, SOPs, allowed/forbidden use cases, and approved examples as text sources for retrieval-grounded feedback.

### Acceptance Criteria

1. An operator can add a policy/SOP document with source title, document type, body text, and effective date.
2. Each policy update creates a new snapshot ID used by later feedback and reports.
3. Retrieval ingestion stores normalized chunks with source document ID, section path, snapshot ID, and index schema version.
4. The health endpoint exposes active index schema version and index freshness without exposing document text.

### Out Of Scope For v1

- Native PDF parsing.
- Google Drive, Notion, or LMS sync as a required launch path.
- Multimodal document indexing.

## Feature: Cohorts And Enrollment

### Description

Operators launch a cohort for a role pack and enroll learners. Learners receive mission assignments and managers can see progress.

### Acceptance Criteria

1. An operator can create a cohort with role pack version, manager, learner list, start date, and due date.
2. Enrolled learners receive one assignment per active mission in the selected role-pack version.
3. A learner cannot submit to a mission unless enrolled in the owning cohort.
4. Cohort progress is computed from deterministic assignment and review states.

### Out Of Scope For v1

- HRIS integration.
- Bulk SSO provisioning.
- Cross-company cohort sharing.

## Feature: Guardrail Quizzes

### Description

Learners answer guardrail questions that test policy boundaries, verification behavior, and forbidden AI use cases.

### Acceptance Criteria

1. A guardrail quiz stores questions, answer choices, correct answers, explanation text, and pass threshold.
2. Quiz scoring is deterministic and produces score, pass/fail, and missed question IDs.
3. A mission can require a passing guardrail quiz before feedback is released.
4. Quiz results are included in manager dashboard metrics.

### Out Of Scope For v1

- Proctored exams.
- Regulated certification.
- Adaptive testing.

## Feature: Learner Submissions

### Description

Learners submit text artifacts from real workflows. The system stores the artifact, checks for sensitive-data indicators, and routes the submission for feedback or manager review.

### Acceptance Criteria

1. A learner can submit text, answer required reflection fields, and attach the submission to one mission assignment.
2. The system records submission timestamp, policy snapshot ID, rubric ID, redaction status, and review state.
3. Sensitive-data checks can block feedback generation and route the submission to manager review.
4. A learner can revise a submission while preserving prior submission history.

### Out Of Scope For v1

- File uploads.
- Screenshots or video walkthroughs.
- Spreadsheet parsing.

## Feature: AI-Assisted Rubric Feedback

### Description

The feedback service retrieves policy/SOP evidence, evaluates the submitted artifact against a rubric, and stores structured feedback with citations and risk flags.

### Acceptance Criteria

1. Feedback output contains rubric outcome, evidence citations, learner-facing feedback, manager notes, risk flags, and validation status.
2. Feedback generation returns `insufficient_evidence` when retrieval does not meet evidence threshold.
3. Feedback does not set final certification or manager approval state.
4. Failed feedback jobs are retryable without creating duplicate feedback records.

### Out Of Scope For v1

- Fully automated certification.
- Uncited policy guidance.
- Autonomous policy edits.

## Feature: Manager Review And Approvals

### Description

Managers review submissions, feedback, risks, and suggested workflow changes, then approve or reject repeatable adoption evidence.

### Acceptance Criteria

1. A manager can list submissions by learner, mission, guardrail status, feedback status, and risk flag.
2. A manager can approve a workflow change with a note and approval timestamp.
3. Manager approval is stored separately from AI feedback and cannot be set by the feedback job.
4. Rejected submissions preserve the rejection reason and remain visible in cohort history.

### Out Of Scope For v1

- HR performance records.
- Automated disciplinary workflows.
- External manager approval integrations.

## Feature: Dashboard And Reports

### Description

Managers and operators view adoption metrics and export progress reports for a pilot cohort.

### Acceptance Criteria

1. Dashboard shows completion rate, submission rate, guardrail pass rate, manager approval count, feedback backlog, and sensitive-data flag rate.
2. Metrics are computed from stored deterministic records, not from LLM summaries.
3. Exported report includes cohort metadata, role-pack version, policy snapshot, key metrics, approved workflow changes, and open risks.
4. Report generation creates a versioned artifact with an audit event.

### Out Of Scope For v1

- Executive BI integration.
- Multi-cohort benchmarking across companies.
- Billing analytics.

## Feature: Audit And Evidence Trail

### Description

The system stores append-only audit events and evidence pointers so future reviewers can reconstruct how feedback, approvals, and reports were produced.

### Acceptance Criteria

1. Authentication, policy updates, submissions, feedback generation, approvals, report exports, and deletion/redaction actions emit audit events.
2. Audit events include timestamp, actor ID, action, resource type, resource ID, result, and trace ID.
3. Audit records are append-only through application code.
4. Evidence records point to policy snapshot, rubric version, submission version, feedback job ID, and report version.

### Out Of Scope For v1

- Formal SOC 2 evidence package.
- Immutable external ledger.
- Regulated retention attestation.

## Retrieval

### Sources Indexed

- Company AI policy.
- Allowed and forbidden AI use cases.
- Role-specific SOPs.
- Mission rubrics and training content.
- Approved example submissions.

### Query Types Supported

- Single-policy lookup for guardrail questions.
- Multi-document lookup across SOP and policy evidence.
- Multi-hop lookup linking role workflow, rubric expectation, and policy boundary.
- No-answer queries that must return `insufficient_evidence`.

### Retrieval Mode

Text-only. Multimodal retrieval is out of scope until pilot evidence shows text submissions and text source documents are insufficient.

### Citation Format

Feedback citations use source IDs and section references:

```json
{
  "source_id": "policy-2026-05-01",
  "section": "Allowed AI Use / Customer Data",
  "chunk_id": "chunk-018",
  "quote": "short excerpt or normalized snippet"
}
```

### insufficient_evidence Behavior

When retrieval returns too few relevant chunks, stale snapshots, or conflicting evidence, the feedback job stores status `insufficient_evidence`, includes the missing evidence reason, and routes the submission to human review. It must not produce uncited policy guidance.
