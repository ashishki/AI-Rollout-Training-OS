from collections.abc import Sequence

import sqlalchemy as sa
from ai_rollout_os.retrieval.constants import VECTOR_DIMENSIONS
from alembic import op
from pgvector.sqlalchemy import Vector

revision: str = "0007_retrieval_chunks"
down_revision: str | None = "0006_submissions"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    op.create_table(
        "retrieval_corpus_versions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("source_id", sa.String(length=64), nullable=False),
        sa.Column("source_document_id", sa.String(length=64), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("index_schema_version", sa.String(length=16), nullable=False),
        sa.Column("embedding_model", sa.String(length=128), nullable=False),
        sa.Column("embedding_dimensions", sa.Integer(), nullable=False),
        sa.Column("chunk_count", sa.Integer(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_retrieval_corpus_versions_snapshot_id",
        "retrieval_corpus_versions",
        ["snapshot_id"],
    )
    op.create_index(
        "ix_retrieval_corpus_versions_source_id",
        "retrieval_corpus_versions",
        ["source_id"],
    )
    op.create_index(
        "ix_retrieval_corpus_versions_workspace_id",
        "retrieval_corpus_versions",
        ["workspace_id"],
    )

    op.create_table(
        "retrieval_chunks",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("corpus_version_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("source_id", sa.String(length=64), nullable=False),
        sa.Column("source_document_id", sa.String(length=64), nullable=False),
        sa.Column("snapshot_id", sa.String(length=64), nullable=False),
        sa.Column("section_path", sa.String(length=512), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("content_hash", sa.String(length=64), nullable=False),
        sa.Column("token_count", sa.Integer(), nullable=False),
        sa.Column("index_schema_version", sa.String(length=16), nullable=False),
        sa.Column("embedding_model", sa.String(length=128), nullable=False),
        sa.Column("embedding", Vector(VECTOR_DIMENSIONS), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ["corpus_version_id"], ["retrieval_corpus_versions.id"]
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_retrieval_chunks_content_hash", "retrieval_chunks", ["content_hash"]
    )
    op.create_index(
        "ix_retrieval_chunks_corpus_version_id",
        "retrieval_chunks",
        ["corpus_version_id"],
    )
    op.create_index(
        "ix_retrieval_chunks_snapshot_id", "retrieval_chunks", ["snapshot_id"]
    )
    op.create_index("ix_retrieval_chunks_source_id", "retrieval_chunks", ["source_id"])
    op.create_index(
        "ix_retrieval_chunks_workspace_id", "retrieval_chunks", ["workspace_id"]
    )
    op.create_index(
        "ix_retrieval_chunks_embedding_hnsw",
        "retrieval_chunks",
        ["embedding"],
        postgresql_using="hnsw",
        postgresql_ops={"embedding": "vector_cosine_ops"},
    )


def downgrade() -> None:
    op.drop_index("ix_retrieval_chunks_embedding_hnsw", table_name="retrieval_chunks")
    op.drop_index("ix_retrieval_chunks_workspace_id", table_name="retrieval_chunks")
    op.drop_index("ix_retrieval_chunks_source_id", table_name="retrieval_chunks")
    op.drop_index("ix_retrieval_chunks_snapshot_id", table_name="retrieval_chunks")
    op.drop_index(
        "ix_retrieval_chunks_corpus_version_id", table_name="retrieval_chunks"
    )
    op.drop_index("ix_retrieval_chunks_content_hash", table_name="retrieval_chunks")
    op.drop_table("retrieval_chunks")
    op.drop_index(
        "ix_retrieval_corpus_versions_workspace_id",
        table_name="retrieval_corpus_versions",
    )
    op.drop_index(
        "ix_retrieval_corpus_versions_source_id",
        table_name="retrieval_corpus_versions",
    )
    op.drop_index(
        "ix_retrieval_corpus_versions_snapshot_id",
        table_name="retrieval_corpus_versions",
    )
    op.drop_table("retrieval_corpus_versions")
