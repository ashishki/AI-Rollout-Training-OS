# Migration Rehearsal

Version: 1.0
Last updated: 2026-05-21
Owner: Operator on call

Use this checklist before pilot expansion, schema-changing releases, retention
changes, or any migration that touches learner submissions, source documents,
feedback results, audit events, reports, reminders, or integration records.

## Scope

The rehearsal proves that a release can upgrade, validate, roll back, back up,
and restore the database without losing auditability or exposing sensitive text.
All notes must use workspace IDs, cohort IDs, job IDs, document IDs, snapshot
IDs, report IDs, and migration revisions. Do not paste learner artifacts,
policy/SOP body text, manager notes, emails, full names, secrets, or customer
text into rehearsal evidence.

## Pre-Rehearsal Inputs

| Input | Required evidence |
|-------|-------------------|
| Release SHA | Exact git SHA or deployment artifact ID. |
| Current migration revision | `alembic current` output from the source environment. |
| Target migration revision | Expected Alembic head after upgrade. |
| Backup reference | Fresh backup path or object ID created according to `docs/backup_restore.md`. |
| Restore target | Disposable restore database name and connection string. |
| Smoke dataset | Workspace/cohort/report IDs safe for rehearsal validation. |

## Backup Step

1. Create a fresh PostgreSQL backup before running the migration.
2. Store the backup outside the application repository in the controlled backup
   location.
3. Record backup path or object ID, timestamp, database name, and checksum if the
   storage layer provides one.
4. Confirm the backup contains `alembic_version`, audit tables, source documents,
   submissions, feedback jobs/results, reports, reminders, and integration
   tables.

## Upgrade Step

1. Start from a clean restore of the pre-upgrade backup in a disposable database.
2. Run `alembic upgrade head`.
3. Record the previous revision, target revision, final revision, command exit
   code, and migration logs.
4. Confirm the app can import models and create a database session against the
   upgraded schema.
5. Run read-only checks for row counts and key constraints before any write
   validation.

## Validation Step

Validate the upgraded schema before accepting it:

- Run `.venv/bin/pytest tests/integration/test_migrations.py -q`.
- Run a health check against the app factory.
- Run one read-only dashboard/report query for a known cohort.
- Run retrieval eval in `--no-write` mode if retrieval tables or source document
  schema changed.
- Check that audit event count did not decrease.
- Check that no raw learner artifact, policy body, manager note, email, full
  name, secret, or customer text appears in logs, metrics labels, rehearsal
  notes, or alert payloads.
- Confirm queued feedback jobs, reminder jobs, report rows, model registry rows,
  and feedback sampling rows remain readable.

## Rollback Plan

1. Prefer application rollback to the previous container/image when the database
   schema remains backward compatible.
2. If the schema is not backward compatible, stop web and worker processes before
   restoring data.
3. Use the fresh pre-upgrade backup as the rollback source of truth.
4. Preserve the failed upgraded database, logs, and migration output for incident
   review.
5. Record which Alembic revision, application version, and backup restored the
   service.

## Restore Step

1. Create a clean restore database.
2. Restore the rehearsal backup with `pg_restore --clean --if-exists --no-owner`.
3. Run `alembic current` and confirm it matches the expected pre-upgrade
   revision.
4. Run the health check and a read-only dashboard/report query.
5. Confirm restored row counts for audit events, submissions, source documents,
   feedback jobs/results, reports, reminder jobs, and model registry records.
6. Document restore duration and any manual steps.

## Go / No-Go Criteria

Go:
- Backup, upgrade, validation, rollback plan, and restore steps all complete.
- No audit event loss or cross-workspace data exposure is observed.
- Rehearsal evidence includes exact revisions, backup reference, restore result,
  and validation command output.

No-go:
- Backup cannot be restored.
- Migration leaves partial data mutation without a verified rollback path.
- Audit event counts decrease or workspace isolation checks fail.
- Sensitive content appears in logs, metrics labels, notes, or alerts.
- Core health, dashboard/report, migration, or retrieval validation fails.

## Evidence Record

Each rehearsal record must include:

- Date, owner, environment, release SHA, current revision, target revision, and
  final revision.
- Backup reference, restore database, restore duration, and validation commands.
- Go/no-go decision and open follow-up owners.
- Links to incident record if failed migration handling used
  `docs/incident_response.md`.
