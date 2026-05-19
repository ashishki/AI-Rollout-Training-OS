from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0003_documents"
down_revision: str | None = "0002_role_packs"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "source_documents",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("logical_document_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("document_type", sa.String(length=64), nullable=False),
        sa.Column("body_text", sa.Text(), nullable=False),
        sa.Column("effective_date", sa.Date(), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("created_by", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("snapshot_id"),
    )
    op.create_index(
        "ix_source_documents_logical_document_id",
        "source_documents",
        ["logical_document_id"],
    )
    op.create_index(
        "ix_source_documents_workspace_id", "source_documents", ["workspace_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_source_documents_workspace_id", table_name="source_documents")
    op.drop_index(
        "ix_source_documents_logical_document_id", table_name="source_documents"
    )
    op.drop_table("source_documents")
