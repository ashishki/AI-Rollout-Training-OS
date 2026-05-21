import logging

import pytest
from ai_rollout_os.auth.tokens import ActorContext
from ai_rollout_os.db.models import User, Workspace
from ai_rollout_os.integrations.user_import import UserImportError, UserImportService
from sqlalchemy import select
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session


def test_user_import_validates_before_mutation(migrated_engine: Engine) -> None:
    csv_text = "\n".join(
        [
            "user_id,email,full_name,role,manager_id,team",
            "manager-1,manager@example.test,Manager One,manager,,Support",
            "learner-1,learner@example.test,Learner One,admin,manager-1,Support",
        ]
    )

    with Session(migrated_engine) as session:
        with pytest.raises(UserImportError, match="validation failed"):
            UserImportService(session).import_csv(csv_text, _operator_actor())
        session.commit()

    with Session(migrated_engine) as session:
        users = session.scalars(select(User)).all()
    assert users == []


def test_user_import_errors_redact_pii(
    migrated_engine: Engine, caplog: pytest.LogCaptureFixture
) -> None:
    csv_text = "\n".join(
        [
            "user_id,email,full_name,role,manager_id,team",
            "learner-1,alice.private@example.test,Alice Private,"
            "learner,missing-manager,Support",
        ]
    )

    caplog.set_level(logging.WARNING)
    with (
        Session(migrated_engine) as session,
        pytest.raises(UserImportError) as exc_info,
    ):
        UserImportService(session).import_csv(csv_text, _operator_actor())

    assert "alice.private@example.test" not in caplog.text
    assert "Alice Private" not in caplog.text
    assert "alice.private@example.test" not in str(exc_info.value)
    assert "Alice Private" not in str(exc_info.value)


def test_user_import_imports_valid_rows(migrated_engine: Engine) -> None:
    csv_text = "\n".join(
        [
            "user_id,email,full_name,role,manager_id,team",
            "manager-1,manager@example.test,Manager One,manager,,Support",
            "learner-1,learner@example.test,Learner One,learner,manager-1,Support",
            "operator-1,operator@example.test,Operator One,operator,,Operations",
        ]
    )

    with Session(migrated_engine) as session:
        session.add(Workspace(id="ws-1", name="Workspace 1"))
        session.flush()
        result = UserImportService(session).import_csv(csv_text, _operator_actor())
        session.commit()

    assert result.imported_count == 3
    assert result.role_counts == {"learner": 1, "manager": 1, "operator": 1}
    assert result.teams == ["Operations", "Support"]
    assert result.manager_links == {"learner-1": "manager-1"}
    with Session(migrated_engine) as session:
        users = session.scalars(select(User).order_by(User.id)).all()
    assert [(user.id, user.email, user.role) for user in users] == [
        ("learner-1", "learner@example.test", "learner"),
        ("manager-1", "manager@example.test", "manager"),
        ("operator-1", "operator@example.test", "operator"),
    ]


def _operator_actor() -> ActorContext:
    return ActorContext(
        actor_id="operator-1",
        role="operator",
        workspace_id="ws-1",
        trace_id="trace-user-import",
    )
