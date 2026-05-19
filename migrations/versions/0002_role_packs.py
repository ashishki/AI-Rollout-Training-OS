from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0002_role_packs"
down_revision: str | None = "0001_foundation"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_table(
        "role_packs",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("role", sa.String(length=128), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.Column("launch_status", sa.String(length=32), nullable=False),
        sa.Column("created_by", sa.String(length=64), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_role_packs_workspace_id", "role_packs", ["workspace_id"])
    op.create_table(
        "rubrics",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_rubrics_workspace_id", "rubrics", ["workspace_id"])
    op.create_table(
        "guardrail_quizzes",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("version", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_guardrail_quizzes_workspace_id", "guardrail_quizzes", ["workspace_id"]
    )
    op.create_table(
        "mission_templates",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("role_pack_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("objective", sa.Text(), nullable=False),
        sa.Column("instructions", sa.Text(), nullable=False),
        sa.Column("artifact_type", sa.String(length=64), nullable=False),
        sa.Column("rubric_id", sa.String(length=64), nullable=False),
        sa.Column("guardrail_quiz_id", sa.String(length=64), nullable=False),
        sa.Column("active", sa.Boolean(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["role_pack_id"], ["role_packs.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_mission_templates_role_pack_id", "mission_templates", ["role_pack_id"]
    )
    op.create_index(
        "ix_mission_templates_workspace_id", "mission_templates", ["workspace_id"]
    )


def downgrade() -> None:
    op.drop_index("ix_mission_templates_workspace_id", table_name="mission_templates")
    op.drop_index("ix_mission_templates_role_pack_id", table_name="mission_templates")
    op.drop_table("mission_templates")
    op.drop_index("ix_guardrail_quizzes_workspace_id", table_name="guardrail_quizzes")
    op.drop_table("guardrail_quizzes")
    op.drop_index("ix_rubrics_workspace_id", table_name="rubrics")
    op.drop_table("rubrics")
    op.drop_index("ix_role_packs_workspace_id", table_name="role_packs")
    op.drop_table("role_packs")
