from sqlalchemy import inspect
from sqlalchemy.engine import Engine


def test_alembic_upgrade_creates_foundation_tables(migrated_engine: Engine) -> None:
    inspector = inspect(migrated_engine)

    assert {"users", "workspaces", "audit_events"}.issubset(inspector.get_table_names())
    audit_columns = {column["name"] for column in inspector.get_columns("audit_events")}
    assert {
        "timestamp",
        "actor_id",
        "action",
        "resource_type",
        "resource_id",
        "result",
        "trace_id",
    }.issubset(audit_columns)
