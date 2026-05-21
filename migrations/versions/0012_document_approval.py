from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0012_document_approval"
down_revision: str | None = "0011_reminders"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "source_documents",
        sa.Column(
            "approval_status",
            sa.String(length=32),
            server_default="pending",
            nullable=False,
        ),
    )
    op.add_column(
        "source_documents",
        sa.Column("approved_by", sa.String(length=64), nullable=True),
    )
    op.add_column(
        "source_documents",
        sa.Column("approved_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("source_documents", "approved_at")
    op.drop_column("source_documents", "approved_by")
    op.drop_column("source_documents", "approval_status")
