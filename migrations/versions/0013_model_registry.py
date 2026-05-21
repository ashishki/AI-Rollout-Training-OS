from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0013_model_registry"
down_revision: str | None = "0012_document_approval"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "feedback_results",
        sa.Column(
            "prompt_version",
            sa.String(length=128),
            server_default="untracked",
            nullable=False,
        ),
    )
    op.add_column(
        "feedback_results",
        sa.Column(
            "model_version",
            sa.String(length=128),
            server_default="untracked",
            nullable=False,
        ),
    )
    op.add_column(
        "feedback_results",
        sa.Column(
            "rubric_version",
            sa.String(length=128),
            server_default="untracked",
            nullable=False,
        ),
    )
    op.add_column(
        "feedback_results",
        sa.Column(
            "corpus_version",
            sa.String(length=128),
            server_default="untracked",
            nullable=False,
        ),
    )
    op.add_column(
        "feedback_results",
        sa.Column(
            "feedback_schema_version",
            sa.String(length=128),
            server_default="untracked",
            nullable=False,
        ),
    )
    op.create_table(
        "model_registry_records",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("registry_type", sa.String(length=64), nullable=False),
        sa.Column("version", sa.String(length=128), nullable=False),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("registry_metadata", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("workspace_id", "registry_type", "version"),
    )
    op.create_index(
        "ix_model_registry_records_workspace_id",
        "model_registry_records",
        ["workspace_id"],
    )


def downgrade() -> None:
    op.drop_index(
        "ix_model_registry_records_workspace_id",
        table_name="model_registry_records",
    )
    op.drop_table("model_registry_records")
    op.drop_column("feedback_results", "feedback_schema_version")
    op.drop_column("feedback_results", "corpus_version")
    op.drop_column("feedback_results", "rubric_version")
    op.drop_column("feedback_results", "model_version")
    op.drop_column("feedback_results", "prompt_version")
