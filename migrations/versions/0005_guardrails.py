from collections.abc import Sequence

import sqlalchemy as sa
from alembic import op

revision: str = "0005_guardrails"
down_revision: str | None = "0004_cohorts"
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.add_column(
        "guardrail_quizzes",
        sa.Column("pass_threshold", sa.Integer(), nullable=False, server_default="80"),
    )
    op.alter_column("guardrail_quizzes", "pass_threshold", server_default=None)
    op.create_table(
        "guardrail_questions",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("quiz_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("question_text", sa.Text(), nullable=False),
        sa.Column("answer_choices", sa.JSON(), nullable=False),
        sa.Column("correct_answer_ids", sa.JSON(), nullable=False),
        sa.Column("explanation", sa.Text(), nullable=False),
        sa.ForeignKeyConstraint(["quiz_id"], ["guardrail_quizzes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        "ix_guardrail_questions_quiz_id", "guardrail_questions", ["quiz_id"]
    )
    op.create_index(
        "ix_guardrail_questions_workspace_id", "guardrail_questions", ["workspace_id"]
    )
    op.create_table(
        "quiz_results",
        sa.Column("id", sa.String(length=64), nullable=False),
        sa.Column("quiz_id", sa.String(length=64), nullable=False),
        sa.Column("workspace_id", sa.String(length=64), nullable=False),
        sa.Column("learner_id", sa.String(length=64), nullable=False),
        sa.Column("score", sa.Integer(), nullable=False),
        sa.Column("passed", sa.Boolean(), nullable=False),
        sa.Column("missed_question_ids", sa.JSON(), nullable=False),
        sa.Column("answers", sa.JSON(), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["quiz_id"], ["guardrail_quizzes.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_quiz_results_quiz_id", "quiz_results", ["quiz_id"])
    op.create_index("ix_quiz_results_learner_id", "quiz_results", ["learner_id"])
    op.create_index("ix_quiz_results_workspace_id", "quiz_results", ["workspace_id"])


def downgrade() -> None:
    op.drop_index("ix_quiz_results_workspace_id", table_name="quiz_results")
    op.drop_index("ix_quiz_results_learner_id", table_name="quiz_results")
    op.drop_index("ix_quiz_results_quiz_id", table_name="quiz_results")
    op.drop_table("quiz_results")
    op.drop_index(
        "ix_guardrail_questions_workspace_id", table_name="guardrail_questions"
    )
    op.drop_index("ix_guardrail_questions_quiz_id", table_name="guardrail_questions")
    op.drop_table("guardrail_questions")
    op.drop_column("guardrail_quizzes", "pass_threshold")
