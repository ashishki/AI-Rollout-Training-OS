from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0011_reminders"
down_revision: str | None = "0010_reports"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "reminder_jobs",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("reminder_type", sa.String(length=64), nullable=False),
        sa.Column("idempotency_key", sa.String(length=192), nullable=False),
        sa.Column("recipient_id", sa.String(length=64), nullable=False),
        sa.Column("assignment_id", sa.String(length=64), nullable=True),
        sa.Column("submission_id", sa.String(length=64), nullable=True),
        sa.Column("feedback_job_id", sa.String(length=64), nullable=True),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("delivery_channel", sa.String(length=32), nullable=True),
        sa.Column("due_date", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index(
        "ix_reminder_jobs_assignment_id", "reminder_jobs", ["assignment_id"]
    )
    op.create_index(
        "ix_reminder_jobs_feedback_job_id",
        "reminder_jobs",
        ["feedback_job_id"],
    )
    op.create_index("ix_reminder_jobs_recipient_id", "reminder_jobs", ["recipient_id"])
    op.create_index(
        "ix_reminder_jobs_submission_id", "reminder_jobs", ["submission_id"]
    )
    op.create_index("ix_reminder_jobs_workspace_id", "reminder_jobs", ["workspace_id"])


def downgrade() -> None:
    op.drop_index("ix_reminder_jobs_workspace_id", table_name="reminder_jobs")
    op.drop_index("ix_reminder_jobs_submission_id", table_name="reminder_jobs")
    op.drop_index("ix_reminder_jobs_recipient_id", table_name="reminder_jobs")
    op.drop_index("ix_reminder_jobs_feedback_job_id", table_name="reminder_jobs")
    op.drop_index("ix_reminder_jobs_assignment_id", table_name="reminder_jobs")
    op.drop_table("reminder_jobs")
