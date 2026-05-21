# Incident Response Runbook

Version: 1.0
Last updated: 2026-05-21
Owner: Operator on call

Use this runbook for reliability and security incidents in AI Rollout Training
OS. Keep all incident notes, logs, dashboards, and alert payloads free of raw
prompts, learner artifacts, policy/SOP body text, manager notes, emails, full
names, and customer text. Use workspace IDs, cohort IDs, job IDs, document IDs,
snapshot IDs, model names, and feature names instead.

## Severity And Escalation

| Severity | When to use | Escalation |
|----------|-------------|------------|
| SEV-1 | Data leak suspicion, cross-workspace access, failed migration blocking writes, persistent 5xx outage, or any incident with regulatory exposure. | Page operator on call immediately, appoint incident commander, preserve audit logs, stop affected processing, notify project owner, and prepare customer/security notification draft. |
| SEV-2 | Retrieval outage, feedback job backlog, provider degradation, sustained latency burn, or repeated retryable failures affecting pilot users. | Page operator on call, assign technical lead, post status every 30 minutes, and open a follow-up ticket before closure. |
| SEV-3 | Degraded metrics below paging threshold, isolated failed jobs, or non-urgent documentation/process gaps. | Create reliability ticket, assign owner, and review in the next operations check. |

## Common First Response

1. Acknowledge the alert and record incident start time.
2. Assign severity, incident commander, technical lead, and scribe.
3. Identify affected workspace IDs, cohort IDs, job IDs, route names, provider,
   model, feature, corpus version, and migration revision.
4. Preserve logs, audit events, deployment metadata, migration revision, and
   relevant dashboard snapshots.
5. Stop or disable only the affected processing path when possible.
6. Communicate status using IDs and symptoms, not sensitive content.
7. Track every mitigation, owner, and timestamp in the incident notes.

## Retrieval Outage

Symptoms:
- Retrieval query errors or timeouts.
- Retrieval p95/p99 latency burn from `docs/slo.md`.
- Feedback jobs routed to human review because evidence is unavailable.

Containment:
1. Confirm whether the outage affects one workspace, one corpus version, or all
   retrieval queries.
2. Disable automatic feedback release for affected workspaces if evidence lookup
   is unreliable.
3. Route new submissions to manager review or `needs_human_review`.
4. Preserve corpus version IDs, source document snapshot IDs, and retrieval error
   traces.

Diagnosis:
1. Check PostgreSQL/pgvector availability and current migration revision.
2. Compare failing corpus versions with `docs/retrieval_eval.md` history.
3. Re-run retrieval eval in no-write mode if database availability is stable.
4. Inspect recent document approval or ingestion changes by snapshot ID.

Recovery:
1. Restore database service or rollback the retrieval code/config change.
2. Rebuild embeddings from approved stored snapshots if index data is stale or
   corrupt.
3. Re-run retrieval eval and confirm hit/no-answer metrics and latency recover.
4. Re-enable automatic feedback release only after evidence citation validation
   passes.

## Feedback Job Backlog

Symptoms:
- Feedback queue depth or oldest job age burns the SLO threshold.
- Many jobs remain `queued`, `running`, or `retryable_failed`.
- Learners or managers report missing feedback.

Containment:
1. Pause non-critical new cohort launches if backlog is growing quickly.
2. Keep learner submissions accepted but route delayed feedback to manager review
   if the p95 job latency target cannot be met.
3. Preserve affected job IDs, submission IDs, workspace IDs, model names, and
   failure classes.

Diagnosis:
1. Count queued, running, retryable, timed-out, and completed feedback jobs.
2. Check provider availability, model errors, validation failures, and worker
   process health.
3. Compare retry attempts and timeout reasons across affected jobs.
4. Confirm no duplicate idempotency keys or stuck `running` jobs are blocking
   progress.

Recovery:
1. Restart or scale the worker if the worker is unhealthy.
2. Re-run retryable jobs after provider recovery.
3. Mark unrecoverable jobs for human review without deleting originals.
4. Confirm queue depth and oldest job age return below SLO ticket thresholds.

## Data Leak Suspicion

Symptoms:
- Possible cross-workspace access, sensitive text in logs/metrics/exports, or
  unapproved policy/SOP text exposed through retrieval or reports.
- Any report of customer text, learner artifact text, email, full name, or secret
  appearing outside its intended boundary.

Containment:
1. Treat as SEV-1 until disproven.
2. Stop the affected route, worker, export, integration, or retrieval path.
3. Preserve append-only audit events and raw evidence in restricted access.
4. Rotate secrets if credentials, tokens, or provider keys may be exposed.

Diagnosis:
1. Identify affected workspace IDs, actor IDs, resource IDs, and timestamps.
2. Check auth boundary, workspace filters, retrieval snapshot filters, export
   payloads, logs, traces, and metric labels.
3. Determine whether data left the system through a webhook, export, dashboard,
   report, or provider call.
4. Do not copy sensitive text into incident notes; reference restricted evidence
   locations and IDs.

Recovery:
1. Patch the boundary issue and add regression tests before re-enabling traffic.
2. Revoke or rotate exposed credentials and integration webhooks.
3. Notify required internal/customer contacts using the approved security process.
4. Record root cause, affected IDs, containment time, remediation, and follow-up
   controls.

## Failed Migrations

Symptoms:
- Migration command fails, service cannot start due to schema mismatch, or writes
  fail after deploy.
- Alembic revision differs between app expectation and database state.

Containment:
1. Stop rollout and prevent additional schema writes.
2. Preserve database backup reference, migration logs, current revision, target
   revision, and deploy SHA.
3. If writes are failing, put the affected environment into maintenance mode.

Diagnosis:
1. Inspect failed migration revision and prior revision.
2. Confirm whether the failure happened before or after data mutation.
3. Run read-only validation queries against affected tables.
4. Check backup availability and restore procedure in `docs/backup_restore.md`.

Recovery:
1. If no mutation occurred, fix the migration and re-run from the previous
   revision.
2. If partial mutation occurred, follow the documented rollback or restore plan.
3. Validate schema, row counts, constraints, and core pilot path after recovery.
4. Do not resume deploy until backup, restore, and validation evidence is attached
   to the incident record.

## Provider Degradation

Symptoms:
- AI provider timeouts, elevated model errors, cost spike, or degraded latency.
- Feedback worker retries increase while local services remain healthy.

Containment:
1. Route affected features to fallback behavior or manager review.
2. Disable non-critical AI paths if cost or latency burn continues.
3. Preserve provider, model, feature, workspace ID, operation ID, error class,
   and cost/latency metric samples.

Diagnosis:
1. Compare provider errors by model and feature.
2. Check whether errors affect one workspace, one model, one feature, or all
   provider calls.
3. Confirm local validation, schema parsing, and retrieval evidence assembly are
   not the root cause.
4. Review recent prompt/model registry changes.

Recovery:
1. Switch to a configured fallback model or deterministic manager-review path.
2. Re-run a small sample of failed jobs after provider recovery.
3. Confirm feedback validation, cost rate, and p95 latency return to target.
4. Document whether model, prompt, budget, or retry policy changes are needed.

## Closure Checklist

- Incident severity, start time, end time, owner, affected IDs, and root cause
  are recorded.
- Customer/security notification decision is recorded.
- Regression tests or doc updates are linked.
- Metrics recovered below SLO ticket thresholds.
- Follow-up owners and due dates are assigned.
- `docs/IMPLEMENTATION_JOURNAL.md` is updated if the incident changes operating
  assumptions, SLOs, architecture, or task priorities.
