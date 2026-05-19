from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0004_cohorts"
down_revision: str | None = "0003_documents"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "cohorts",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("role_pack_id", sa.String(length=64), nullable=False),
        sa.Column("role_pack_version", sa.Integer(), nullable=False),
        sa.Column("manager_id", sa.String(length=64), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=False),
        sa.Column("due_date", sa.Date(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column("created_by", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cohorts_role_pack_id", "cohorts", ["role_pack_id"])
    op.create_index("ix_cohorts_workspace_id", "cohorts", ["workspace_id"])
    op.create_table(
        "cohort_enrollments",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("cohort_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("learner_id", sa.String(length=64), nullable=False),
        sa.ForeignKeyConstraint(["cohort_id"], ["cohorts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cohort_id", "learner_id"),
    )
    op.create_index(
        "ix_cohort_enrollments_cohort_id", "cohort_enrollments", ["cohort_id"]
    )
    op.create_index(
        "ix_cohort_enrollments_workspace_id",
        "cohort_enrollments",
        ["workspace_id"],
    )
    op.create_table(
        "mission_assignments",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("cohort_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("learner_id", sa.String(length=64), nullable=False),
        sa.Column("mission_template_id", sa.String(length=64), nullable=False),
        sa.Column("role_pack_version", sa.Integer(), nullable=False),
        sa.Column("status", sa.String(length=32), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["cohort_id"], ["cohorts.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("cohort_id", "learner_id", "mission_template_id"),
    )
    op.create_index(
        "ix_mission_assignments_cohort_id", "mission_assignments", ["cohort_id"]
    )
    op.create_index(
        "ix_mission_assignments_learner_id", "mission_assignments", ["learner_id"]
    )
    op.create_index(
        "ix_mission_assignments_workspace_id", "mission_assignments", ["workspace_id"]
    )


def downgrade() -> None:
    op.drop_index(
        "ix_mission_assignments_workspace_id", table_name="mission_assignments"
    )
    op.drop_index("ix_mission_assignments_learner_id", table_name="mission_assignments")
    op.drop_index("ix_mission_assignments_cohort_id", table_name="mission_assignments")
    op.drop_table("mission_assignments")
    op.drop_index("ix_cohort_enrollments_workspace_id", table_name="cohort_enrollments")
    op.drop_index("ix_cohort_enrollments_cohort_id", table_name="cohort_enrollments")
    op.drop_table("cohort_enrollments")
    op.drop_index("ix_cohorts_workspace_id", table_name="cohorts")
    op.drop_index("ix_cohorts_role_pack_id", table_name="cohorts")
    op.drop_table("cohorts")
