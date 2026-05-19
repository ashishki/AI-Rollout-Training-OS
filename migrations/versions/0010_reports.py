from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0010_reports"
down_revision: str | None = "0009_manager_review"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "progress_reports",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("cohort_id", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("role_pack_version", sa.Integer(), nullable=False),
        sa.Column("policy_snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("dashboard_metrics", sa.JSON(), nullable=False),
        sa.Column("markdown_body", sa.Text(), nullable=False),
        sa.Column("json_body", sa.JSON(), nullable=False),
        sa.Column("created_by", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_progress_reports_cohort_id", "progress_reports", ["cohort_id"])
    op.create_index(
        "ix_progress_reports_workspace_id", "progress_reports", ["workspace_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_progress_reports_workspace_id", table_name="progress_reports")
    op.drop_index("ix_progress_reports_cohort_id", table_name="progress_reports")
    op.drop_table("progress_reports")
