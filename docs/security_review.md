# Security Review Packet

Status: Phase 8 review-ready packet.
Last updated: 2026-05-20

## Architecture

AI Rollout Training OS is a T1 pilot deployment with a FastAPI web process,
bounded worker entry points, PostgreSQL/pgvector durable storage, and
server-rendered operator, learner, and manager UI routes. The deployment is
single-company per pilot. Records carry `workspace_id`, but the product does not
claim SaaS-grade multi-tenancy without a future ADR and isolation tests.

The runtime does not install packages, execute shell commands from product code,
mutate host services, or run autonomous external AI workers. AI feedback remains
bounded by stored submissions, retrieved policy/SOP evidence, and human approval
boundaries.

## Data Flow

1. Operators create policy/SOP source documents, role packs, guardrail quizzes,
   mission templates, and cohorts.
2. Learners read assignments, complete guardrail quizzes, and submit artifacts.
3. Sensitive-data detection flags risky artifacts before feedback release.
4. Retrieval ingestion indexes approved policy/SOP source documents into
   workspace-scoped pgvector chunks.
5. Feedback jobs assemble retrieved evidence and produce structured feedback or
   `insufficient_evidence`.
6. Managers review submissions, approve workflow changes, view dashboards, and
   create progress reports.
7. Retention jobs redact expired mutable text while preserving append-only audit
   events.

Raw learner artifacts, policy/SOP bodies, manager notes, and provider secrets
must not appear in logs, span attributes, metrics labels, client errors, or audit
details.

## Subprocessors

| Subprocessor | Purpose | Data shared | Status |
|--------------|---------|-------------|--------|
| PostgreSQL/pgvector | Durable application database and retrieval index | Application records, source documents, submissions, embeddings, audit events | Required |
| Configured AI provider | Bounded feedback and embedding generation | Redacted/allowed prompt context and retrieved evidence, depending on job type | Required for feedback jobs |
| Reminder delivery adapter | Optional learner/manager reminders | Recipient IDs and reminder metadata only | Disabled by default |

No other runtime network egress is approved for v1.

## Secrets Management

Secrets are environment-only and deployment-owned. Required production variables
include `DATABASE_URL`, `SECRET_KEY`, `AI_PROVIDER_API_KEY`, `MODEL_FAST`,
`MODEL_STRONG`, and `EMBEDDING_MODEL`. SSO deployments also require
`OIDC_ISSUER_URL`, `OIDC_CLIENT_ID`, `OIDC_CLIENT_SECRET`, and
`OIDC_REDIRECT_URI`.

Repository files may contain placeholder names such as
`replace-with-oidc-client-secret`, but must not contain real credentials.
Configuration error messages report missing variable names only.

## Identity And SSO

The v1 SSO boundary supports OIDC-based identity verification. The OIDC
provider verifies the external user identity, and the application maps that
verified identity to an existing internal `users` row. Workspace and role values
come only from server-owned user records; client-provided role or workspace
claims are ignored.

Required OIDC configuration is read from deployment environment variables:

- `SSO_ENABLED`
- `OIDC_ISSUER_URL`
- `OIDC_CLIENT_ID`
- `OIDC_CLIENT_SECRET`
- `OIDC_REDIRECT_URI`

`OIDC_CLIENT_SECRET` is never stored in source files, committed configuration,
logs, audit event details, or client responses. Missing SSO configuration errors
report only variable names.

## SAML Decision Path

SAML is deferred until a buyer requires it during procurement. The decision path
for adding SAML is:

1. Confirm the customer identity provider requires SAML rather than OIDC.
2. Record the supported IdP metadata exchange, signing certificate rotation,
   attribute mapping, and single logout requirements.
3. Keep the same server-side identity boundary: SAML attributes may identify a
   user, but application roles and workspaces still come from server-owned user
   mappings.
4. Add an ADR before enabling SAML in production.

## RBAC Permission Matrix

Every protected route maps to one named permission. Permission checks run after
authentication and before service-layer mutation. Denied permission checks emit
`denied_access` audit events with `resource_type=permission` and the permission
name as `resource_id`.

| Permission | Roles |
|------------|-------|
| `app.shell.view` | learner, manager, operator |
| `app.operator.view` | operator |
| `app.learner.view` | learner |
| `app.manager.view` | manager |
| `app.operator.documents.create` | operator |
| `app.operator.guardrail_quizzes.create` | operator |
| `app.operator.role_packs.create` | operator |
| `app.operator.missions.create` | operator |
| `app.operator.role_packs.launch` | operator |
| `app.operator.cohorts.create` | operator |
| `app.operator.cohorts.launch` | operator |
| `app.learner.guardrail_submissions.create` | learner |
| `app.learner.submissions.create` | learner |
| `app.manager.submissions.approve` | manager |
| `app.manager.reports.create` | manager |
| `documents.create` | operator |
| `documents.update` | operator |
| `documents.read_snapshot` | operator |
| `documents.approve` | manager, operator |
| `role_packs.create` | operator |
| `role_packs.missions.create` | operator |
| `role_packs.launch` | operator |
| `role_packs.versions.create` | operator |
| `role_packs.versions.compare` | operator |
| `cohorts.create` | operator |
| `cohorts.launch` | operator |
| `cohorts.assignments.read` | learner |
| `guardrails.create` | operator |
| `guardrails.submissions.create` | learner |
| `guardrails.feedback_release.read` | learner |
| `submissions.create` | learner |
| `submissions.redaction_approval.create` | manager |
| `manager.submissions.read` | manager |
| `manager.submissions.approve` | manager |
| `manager.dashboard.read` | manager |
| `manager.reports.create` | manager |

## Audit Logs

Audit events are append-only application records. Security-relevant events
include authentication denials, permission denials, workspace mismatches,
submission creation, redaction approval, feedback jobs, manager approvals,
report generation, reminders, SSO login, and `retention.redacted` events.

Policy and SOP document versions default to `pending` and are excluded from
active feedback retrieval until a human-owned approval route records
`document.approved`.

Audit records include actor ID when available, action, resource type, resource
ID, result, trace ID, and optional details. Details must not contain raw
submission text, policy/SOP bodies, manager notes, or secrets.

## Controls

| Control area | Implemented control | Evidence |
|--------------|---------------------|----------|
| Authentication | Signed bearer tokens plus OIDC identity boundary | `tests/integration/test_auth.py`, `tests/integration/test_sso.py` |
| Authorization | Named permission matrix for every protected route | `tests/test_permissions_matrix.py` |
| Workspace boundary | Workspace-scoped service queries and denial before mutation | `tests/integration/test_auth.py` |
| Secrets | Env-only config and placeholder-only examples | `tests/unit/test_config.py`, `tests/test_sso_config.py` |
| PII and sensitive data | Deterministic redaction gate and safe UI/log behavior | `tests/integration/test_redaction.py`, `tests/e2e/test_learner_missions.py` |
| Retrieval safety | Workspace/snapshot filters and `insufficient_evidence` | `tests/integration/test_retrieval_query.py`, `scripts/eval.py` |
| Human approval | Manager-owned approval routes only | `tests/integration/test_manager_review.py` |
| Backup and restore | PostgreSQL backup/restore/rollback procedure | `docs/backup_restore.md`, `tests/test_backup_restore_doc.py` |
| Retention | Expired mutable text redaction with audit preservation | `tests/integration/test_retention.py` |

## Incident Response

Security incidents are handled by severity and first containment:

1. Stop affected web/worker processes or disable the affected integration.
2. Preserve logs, database backups, and audit event state.
3. Rotate affected environment secrets through the deployment secret store.
4. Restore from the latest known-good backup when data corruption or unsafe
   retention is suspected.
5. Record the incident, root cause, affected resource IDs, remediation, and
   follow-up tests before reopening access.

Any suspected secret exposure is treated as a security incident even if the
secret is a test value.

## Current Gaps

The packet is sufficient for early pilot IT review. Remaining gaps before
GA-grade security review are formal access review export, SaaS-grade tenant
isolation, audit log tamper evidence beyond append-only application behavior,
and customer-specific subprocessors and incident contacts.
