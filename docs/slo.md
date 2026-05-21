# Service SLOs

Version: 1.0
Last updated: 2026-05-21
Owner: Operator on call

This document defines pilot and expansion reliability targets for AI Rollout
Training OS. Metrics must use opaque workspace, cohort, job, route, model, and
feature labels only. Do not place prompt text, learner artifacts, policy bodies,
manager notes, emails, names, or customer text in metric labels.

## Service Health Metrics

| Metric | Label set | Source | Purpose |
|--------|-----------|--------|---------|
| API latency p95/p99 | route, method, status_class, workspace_id | web request middleware or gateway logs | Detect slow operator, learner, manager, and report workflows. |
| API error rate | route, method, status_class, workspace_id | web request middleware or gateway logs | Detect elevated 5xx and unexpected 4xx failures. |
| Feedback job latency p95/p99 | job_type, status, model, workspace_id | feedback worker job records | Detect slow AI feedback generation and review routing. |
| Retrieval latency p95/p99 | retrieval_mode, corpus_version, workspace_id | retrieval query instrumentation and eval runs | Detect slow policy/SOP evidence lookup. |
| Queue depth | queue_name, status, workspace_id | feedback and reminder job tables | Detect backlog before learner feedback becomes stale. |
| Oldest job age | queue_name, status, workspace_id | feedback and reminder job tables | Detect stuck jobs even when queue depth is small. |
| AI cost rate | provider, model, feature, workspace_id | `AIMetricsLedger` or production metrics sink | Detect runaway usage by model and feature. |

## SLO Targets

| User journey / system path | Objective | Initial target |
|----------------------------|-----------|----------------|
| Health endpoint | Availability | 99.9% monthly successful `GET /health` responses. |
| Authenticated API | Latency | p95 under 750 ms and p99 under 2,000 ms for non-AI request handlers. |
| Retrieval query | Latency | p95 under 500 ms and p99 under 1,500 ms for text-only policy/SOP retrieval. |
| Feedback worker | Latency | p95 under 60 seconds from queued job to terminal status. |
| Reminder scheduler | Freshness | p95 due reminder scheduling under 10 minutes from due scan start. |
| Error rate | Reliability | 5xx rate below 1% over 30 minutes and below 0.2% over 24 hours. |
| Feedback queue depth | Reliability | Fewer than 25 queued or retryable feedback jobs per workspace during pilot. |
| Oldest feedback job age | Reliability | No queued or retryable feedback job older than 15 minutes during pilot. |

## Burn-Rate Signals

Use burn-rate alerts to page on sustained SLO budget burn and to ticket on slow
drift. Initial alert windows are intentionally simple until production traffic
establishes real baselines.

| Signal | Page threshold | Ticket threshold |
|--------|----------------|------------------|
| API error budget burn | 5xx rate >= 5% for 10 minutes | 5xx rate >= 1% for 30 minutes |
| API latency burn | p99 >= 4,000 ms for 10 minutes | p95 >= 1,500 ms for 30 minutes |
| Retrieval latency burn | p99 >= 3,000 ms for 10 minutes | p95 >= 1,000 ms for 30 minutes |
| Feedback job latency burn | p95 queued-to-terminal latency >= 120 seconds for 15 minutes | p95 queued-to-terminal latency >= 90 seconds for 30 minutes |
| Queue depth burn | Any workspace has >= 100 queued/retryable feedback jobs for 10 minutes | Any workspace has >= 25 queued/retryable feedback jobs for 30 minutes |
| Oldest job age burn | Oldest queued/retryable feedback job age >= 30 minutes | Oldest queued/retryable feedback job age >= 15 minutes |
| AI cost burn | Cost rate exceeds workspace budget by 2x for 30 minutes | Cost rate exceeds workspace budget by 1.25x for 2 hours |

## Escalation Rules

| Severity | Trigger | Required action | Owner |
|----------|---------|-----------------|-------|
| SEV-1 | Data leak suspicion, cross-workspace access, persistent 5xx outage, or failed migration blocking writes | Stop affected processing, preserve audit logs, page operator on call, notify incident commander, and start incident response runbook. | Operator on call |
| SEV-2 | Feedback job backlog, retrieval latency burn, API latency burn, provider degradation, or repeated retryable failures | Page operator on call, identify affected workspace/cohort IDs, disable non-critical AI paths if needed, and post 30-minute updates. | Operator on call |
| SEV-3 | Ticket-threshold burn without user-visible outage | Create reliability ticket, attach metrics, assign owner, and review in next operations check. | Owning engineer |

## Dashboard Requirements

- Show current API p95/p99 latency, API error rate, retrieval p95/p99 latency,
  feedback job p95/p99 latency, feedback queue depth, oldest job age, reminder
  queue depth, and AI cost rate.
- Filter by workspace ID, cohort ID where available, route, queue name, provider,
  model, feature, and status class.
- Never include raw prompts, learner artifacts, policy/SOP body text, manager
  notes, emails, full names, or customer text in labels, dashboards, logs, or
  alert payloads.
- Link every paging alert to this document and the incident response runbook once
  the runbook exists.

## Review Cadence

- Review targets after each load test, restore drill, and pilot expansion.
- Tighten or relax targets only with evidence in `docs/IMPLEMENTATION_JOURNAL.md`.
- Re-check this document at each Phase 12 reliability task boundary.
