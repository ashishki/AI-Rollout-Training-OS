# Backup, Restore, Retention, And Rollback

Status: Phase 8 pilot procedure
Last updated: 2026-05-20

## Backup Procedure

Pilot deployments use PostgreSQL as the durable source of truth. Before any
upgrade, migration, or retention run, create a compressed custom-format backup:

```bash
pg_dump --format=custom --no-owner --no-acl \
  --file backups/ai_rollout_$(date +%Y%m%d%H%M%S).dump \
  "$DATABASE_URL"
```

Store backup artifacts in the deployment-controlled backup location, encrypted
at rest. Do not store backups in the application repository.

## Restore Procedure

Restore into an empty PostgreSQL database, then run application smoke checks:

```bash
createdb ai_rollout_restore_check
pg_restore --clean --if-exists --no-owner --dbname ai_rollout_restore_check \
  backups/ai_rollout_YYYYMMDDHHMMSS.dump
```

After restore, run the health check and a read-only report/dashboard query before
accepting the database as a rollback target.

## Retention Procedure

Retention redacts mutable artifact data after the configured retention window.
The retention job redacts submission artifact text, manager free-text fields,
learner feedback, source document bodies, and retrieval chunk text. It does not
delete rows from `audit_events`; audit evidence remains append-only.

Each redaction writes a `retention.redacted` audit event with the affected
resource type and ID. Retention must run only after a fresh backup exists.

## Rollback Procedure

If a deployment or retention run fails, stop web and worker processes, restore
the most recent known-good backup into a clean database, point the deployment to
the restored database, and run smoke checks before reopening access.

Rollback decisions must preserve the failed-run backup and all available logs so
the incident can be reviewed after service is restored.
