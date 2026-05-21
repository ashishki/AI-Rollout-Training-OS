from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0014_feedback_sampling"
down_revision: str | None = "0013_model_registry"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "feedback_sample_reviews",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("feedback_result_id", sa.String(length=64), nullable=False),
        sa.Column("submission_id", sa.String(length=64), nullable=False),
        sa.Column("status", sa.String(length=64), nullable=False),
        sa.Column("sampled_by", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_feedback_sample_reviews_workspace_id",
        "feedback_sample_reviews",
        ["workspace_id"],
    )
    op.create_table(
        "feedback_adjudication_labels",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("sample_review_id", sa.String(length=64), nullable=False),
        sa.Column("feedback_result_id", sa.String(length=64), nullable=False),
        sa.Column("adjudicator_id", sa.String(length=64), nullable=False),
        sa.Column("faithfulness_label", sa.String(length=32), nullable=False),
        sa.Column("completeness_label", sa.String(length=32), nullable=False),
        sa.Column("relevance_label", sa.String(length=32), nullable=False),
        sa.Column("unsupported_claim", sa.Boolean(), nullable=False),
        sa.Column("eval_dataset_record", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_feedback_adjudication_labels_workspace_id",
        "feedback_adjudication_labels",
        ["workspace_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_feedback_adjudication_labels_workspace_id",
        table_name="feedback_adjudication_labels",
    )
    op.drop_table("feedback_adjudication_labels")
    op.drop_index(
        "ix_feedback_sample_reviews_workspace_id",
        table_name="feedback_sample_reviews",
    )
    op.drop_table("feedback_sample_reviews")
