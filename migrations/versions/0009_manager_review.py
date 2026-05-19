from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0009_manager_review"
down_revision: str | None = "0008_jobs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "submissions",
        sa.Column(
            "approval_status",
            sa.String(length=64),
            server_default="not_reviewed",
            nullable=False,
        ),
    )
    op.add_column("submissions", sa.Column("approval_note", sa.Text(), nullable=True))
    op.add_column(
        "submissions", sa.Column("manager_id", sa.String(length=64), nullable=True)
    )
    op.add_column(
        "submissions",
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
    )
    op.add_column(
        "submissions", sa.Column("approved_workflow_change", sa.Text(), nullable=True)
    )
    op.add_column(
        "submissions", sa.Column("rejection_reason", sa.Text(), nullable=True)
    )
    op.add_column(
        "feedback_results",
        sa.Column(
            "risk_flags",
            sa.JSON(),
            server_default=sa.text("'[]'::json"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_column("feedback_results", "risk_flags")
    op.drop_column("submissions", "rejection_reason")
    op.drop_column("submissions", "approved_workflow_change")
    op.drop_column("submissions", "approved_at")
    op.drop_column("submissions", "manager_id")
    op.drop_column("submissions", "approval_note")
    op.drop_column("submissions", "approval_status")
