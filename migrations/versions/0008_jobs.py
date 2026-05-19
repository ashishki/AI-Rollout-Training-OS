from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0008_jobs"
down_revision: str | None = "0007_retrieval_chunks"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "feedback_jobs",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("submission_id", sa.String(length=64), nullable=False),
        sa.Column("submission_version", sa.Integer(), nullable=False),
        sa.Column("idempotency_key", sa.String(length=160), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("attempt_count", sa.Integer(), nullable=False),
        sa.Column("last_error", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("idempotency_key"),
    )
    op.create_index(
        "ix_feedback_jobs_submission_id", "feedback_jobs", ["submission_id"]
    )
    op.create_index("ix_feedback_jobs_workspace_id", "feedback_jobs", ["workspace_id"])

    op.create_table(
        "feedback_results",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("submission_id", sa.String(length=64), nullable=False),
        sa.Column("submission_version", sa.Integer(), nullable=False),
        sa.Column("feedback_status", sa.String(length=64), nullable=False),
        sa.Column("learner_feedback", sa.Text(), nullable=True),
        sa.Column("validation_status", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("submission_id", "submission_version"),
    )
    op.create_index(
        "ix_feedback_results_submission_id",
        "feedback_results",
        ["submission_id"],
    )
    op.create_index(
        "ix_feedback_results_workspace_id",
        "feedback_results",
        ["workspace_id"],
    )


def downgrade() -> None:
    op.drop_index("ix_feedback_results_workspace_id", table_name="feedback_results")
    op.drop_index("ix_feedback_results_submission_id", table_name="feedback_results")
    op.drop_table("feedback_results")
    op.drop_index("ix_feedback_jobs_workspace_id", table_name="feedback_jobs")
    op.drop_index("ix_feedback_jobs_submission_id", table_name="feedback_jobs")
    op.drop_table("feedback_jobs")
