# Pilot Readiness

This checklist is for the first controlled v1 pilot. It is not a production certification gate.

## Required Env Vars

- `APP_ENV`
- `DATABASE_URL`
- `SECRET_KEY`
- `AI_PROVIDER_API_KEY`
- `MODEL_FAST`
- `MODEL_STRONG`
- `EMBEDDING_MODEL`
- `INDEX_MAX_AGE_DAYS`
- `FEEDBACK_TIMEOUT_SECONDS`
- `REMINDER_WINDOW_DAYS`
- `REMINDER_DELIVERY_ENABLED`
- `RETENTION_DAYS`

## Operator Setup Steps

1. Copy `.env.example` to `.env` and replace all placeholder secrets and model names.
2. Run `docker-compose config` and confirm the web, worker, migrate, and postgres services render correctly.
3. Start PostgreSQL and run Alembic migrations with the compose `migrate` service.
4. Create the pilot workspace, operator, manager, and learner accounts.
5. Seed one role pack with two missions, one guardrail quiz, and policy/SOP documents.
6. Launch one cohort, verify assignments, and confirm learner access with signed tokens.
7. Run one bounded feedback/reminder worker cycle and generate a manager report.

## Known Non-Goals

- No production certification or compliance attestation.
- No SaaS-grade tenant isolation beyond workspace-scoped records.
- No external Slack or Telegram reminder delivery unless explicitly enabled and reviewed.
- No productivity guarantee or automated policy/legal approval.
- No autonomous agent loop or runtime shell/package mutation.

## Solo Showcase Mini-Cohort

Phase 15 includes a public-source mini-cohort replay for a synthetic
lead-response operator. The replay is documented in
`docs/solo_showcase_artifacts/mini_cohort_replay.md` and uses one synthetic
learner, one synthetic manager/reviewer, two synthetic submissions, two feedback
results, and one reviewer-approved workflow change.

This replay is demo-only. It does not prove adoption, productivity lift,
compliance readiness, enterprise readiness, paid conversion, or GA readiness.

## Go/No-Go Checks

- Go when migrations, tests, ruff, and retrieval evaluation pass in the target environment.
- Go when the pilot fixture can launch a cohort, accept a submission, generate feedback, record manager approval, and export a report.
- Go for the solo showcase only when the mini-cohort report labels demo data,
  source citations, limitations, and unsupported claims.
- Go when policy/SOP retrieval returns evidence for answerable questions and `insufficient_evidence` for no-answer questions.
- No-go if any required env var still contains a placeholder value in the real `.env`.
- No-go if sensitive learner or customer text appears in logs, metrics labels, audit details, or exported reports.
- No-go if manager approval, legal approval, certification, or productivity claims are automated.
