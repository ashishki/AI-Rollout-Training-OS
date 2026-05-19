from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0006_submissions"
down_revision: str | None = "0005_guardrails"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "submissions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("mission_template_id", sa.String(length=64), nullable=False),
        sa.Column("assignment_id", sa.String(length=64), nullable=False),
        sa.Column("learner_id", sa.String(length=64), nullable=False),
        sa.Column("artifact_text", sa.Text(), nullable=False),
        sa.Column("policy_snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("rubric_id", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("review_state", sa.String(length=64), nullable=False),
        sa.Column("redaction_status", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("assignment_id", "version"),
    )
    op.create_index("ix_submissions_workspace_id", "submissions", ["workspace_id"])
    op.create_index(
        "ix_submissions_mission_template_id", "submissions", ["mission_template_id"]
    )
    op.create_index("ix_submissions_assignment_id", "submissions", ["assignment_id"])
    op.create_index("ix_submissions_learner_id", "submissions", ["learner_id"])


def downgrade() -> None:
    op.drop_index("ix_submissions_learner_id", table_name="submissions")
    op.drop_index("ix_submissions_assignment_id", table_name="submissions")
    op.drop_index("ix_submissions_mission_template_id", table_name="submissions")
    op.drop_index("ix_submissions_workspace_id", table_name="submissions")
    op.drop_table("submissions")
