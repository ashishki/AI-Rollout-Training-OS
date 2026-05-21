# Procurement Packet

Version: 1.0
Last updated: 2026-05-21
Owner: GTM lead

This packet gives buyer, security, IT, procurement, and implementation teams a
single entry point for evaluating AI Rollout Training OS. It summarizes the
current evidence and links to canonical artifacts. Do not paste customer text,
learner artifacts, policy/SOP body text, emails, names, secrets, or credentials
into procurement notes.

## Product Summary

AI Rollout Training OS helps teams launch role-specific AI adoption programs with
policy-grounded missions, guardrail quizzes, learner submissions, structured
feedback, manager approval, reporting, and governance evidence. The initial
buyer is typically VP Support, Enablement, RevOps, AI Transformation, or an
operations leader accountable for safe AI rollout.

Commercial packages are defined in `docs/packaging.md`:

- Team Pilot
- Enterprise Enablement
- Governance Plus
- Regulated Single-Tenant

## Security Packet

Canonical security packet: `docs/security_review.md`.

Covered:
- Architecture and trust boundaries.
- Data flow and storage.
- Secrets management.
- SSO/OIDC identity boundary and SAML decision path.
- RBAC permissions matrix.
- Audit logs and governance controls.
- Backup, restore, retention, and incident response.
- Open security/reliability gaps and customer-specific follow-ups.

Current known caveat:
- Browser automation remains an inherited P2 UX readiness gap before claiming
  browser-rendered GA readiness.

## Privacy And Data Processing Summary

Data categories:
- Workspace IDs, user IDs, emails, roles, cohort IDs, assignment IDs, source
  document snapshots, learner submissions, feedback results, manager approvals,
  report metadata, reminder jobs, audit events, and integration records.

Processing purposes:
- Training assignment delivery.
- Policy/SOP retrieval and evidence citation.
- Feedback generation and validation.
- Manager review and approved workflow tracking.
- Reporting, governance evidence, LMS completion export, HRIS import, and
  reminder delivery.

Controls:
- Sensitive learner text redaction and manager approval flow.
- Source document approval workflow before retrieval evidence becomes active.
- Raw artifact and policy body exclusion from reports, metrics labels, reminder
  payloads, SLO dashboards, and procurement notes.
- Append-only audit events for key actions.
- Retention and backup/restore procedures in `docs/backup_restore.md`.

Subprocessors and external integrations:
- Slack/Teams webhooks are disabled by default and must be explicitly configured.
- HRIS user import is CSV-first.
- LMS completion export omits raw learner artifacts.
- Knowledge imports remain pending until human approval.
- AI provider details depend on customer deployment configuration.

## Deployment Options

| Option | Fit | Notes |
|--------|-----|-------|
| Shared pilot deployment | Team Pilot and early Enterprise Enablement. | Fastest path for pilot validation; does not claim SaaS-grade tenant isolation beyond explicit workspace filtering. |
| Customer-dedicated deployment | Enterprise Enablement or Governance Plus with stronger IT review. | Dedicated database/service boundary can be scoped for customer-specific security needs. |
| Regulated single-tenant | Regulated Single-Tenant package. | Customer-specific infrastructure, backup/restore drill, incident contacts, SSO/SAML/private networking review, and support model. |

Deployment evidence:
- Docker Compose deployment assets: `docker-compose.yml`, `Dockerfile`.
- SLOs: `docs/slo.md`.
- Incident response: `docs/incident_response.md`.
- Migration rehearsal: `docs/migration_rehearsal.md`.

## Support Model

| Support area | Standard expectation |
|--------------|----------------------|
| Pilot setup | Role-pack setup, policy/SOP import, cohort launch, guardrail review, and manager workflow alignment. |
| Security/procurement | Security packet, data-processing summary, deployment option review, and open-gap tracking. |
| Reliability | SLO review, load-test evidence, incident runbook, backup/restore and migration rehearsal evidence. |
| Product operations | Operator admin support, learner mission support, manager review/report support, and governance export support. |
| Escalation | SEV-1/SEV-2/SEV-3 rules in `docs/incident_response.md`. |

## Implementation Plan

1. Confirm buyer, package tier, deployment option, data categories, and success
   metrics.
2. Complete security/procurement review using `docs/security_review.md` and this
   packet.
3. Configure workspace, SSO/OIDC if needed, operator/manager/learner roles, and
   integration settings.
4. Import policy/SOP documents and require human approval before retrieval use.
5. Build role packs, guardrail quizzes, missions, and rubrics.
6. Launch first cohort and monitor activation, completion, manager review SLA,
   risk flags, approved workflow changes, and feedback backlog.
7. Review pilot ROI using customer-provided assumptions and observed pilot
   metrics.
8. Decide expand, repeat, pause, or reposition using
   `docs/pilot_success_rubric.md`.

## Procurement Checklist

- Package tier selected from `docs/packaging.md`.
- Security packet reviewed.
- Privacy and data-processing summary reviewed.
- Deployment option selected.
- Support model and escalation contacts agreed.
- Backup/restore, incident response, and migration rehearsal evidence reviewed.
- Pilot success metrics and ROI assumption owner agreed.
- Open findings accepted or assigned with owners.
