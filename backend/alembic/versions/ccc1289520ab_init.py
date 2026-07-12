"""init

Revision ID: ccc1289520ab
Revises:
Create Date: 2026-07-12 00:00:00.000000

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision: str = "ccc1289520ab"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### users ###
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("email", sa.String(255), nullable=False),
        sa.Column("username", sa.String(50), nullable=True),
        sa.Column("avatar_url", sa.String(), nullable=True),
        sa.Column("password_hash", sa.String(), nullable=True),
        sa.Column("auth_provider", sa.String(20), nullable=False, server_default="email"),
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
        sa.UniqueConstraint("email"),
    )

    # ### user_progress ###
    op.create_table(
        "user_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("stage", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("total_xp", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("level", sa.Integer(), nullable=False, server_default="1"),
        sa.Column("streak_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_active_date", sa.Date(), nullable=True),
        sa.Column("joy_name", sa.String(20), nullable=False, server_default="Joy"),
        sa.Column("joy_gender", sa.String(10), nullable=False, server_default="female"),
        sa.Column("joy_personality", sa.String(20), nullable=False, server_default="gentle"),
        sa.Column("joy_display_mode", sa.String(20), nullable=False, server_default="auto_hide"),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("user_id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    # ### letters ###
    op.create_table(
        "letters",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("char", sa.String(10), nullable=False),
        sa.Column("type", sa.String(30), nullable=False),
        sa.Column("romanization", sa.String(20), nullable=True),
        sa.Column("chinese_hint", sa.Text(), nullable=True),
        sa.Column("pronunciation_audio_url", sa.Text(), nullable=True),
        sa.Column("stroke_animation_url", sa.Text(), nullable=True),
        sa.Column("mouth_shape_url", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("pronunciation_tip", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # ### letter_progress ###
    op.create_table(
        "letter_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("letter_id", sa.String(10), nullable=False),
        sa.Column("letter_type", sa.String(20), nullable=True),
        sa.Column("mastered", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("practice_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("best_score", sa.Float(), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    # ### words ###
    op.create_table(
        "words",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("korean", sa.String(100), nullable=False),
        sa.Column("chinese", sa.String(200), nullable=True),
        sa.Column("romanization", sa.String(200), nullable=True),
        sa.Column("pronunciation_audio_url", sa.Text(), nullable=True),
        sa.Column("category", sa.String(50), nullable=True),
        sa.Column("sub_category", sa.String(50), nullable=True),
        sa.Column("difficulty_level", sa.Integer(), nullable=False, server_default="1"),
        sa.PrimaryKeyConstraint("id"),
    )

    # ### word_examples ###
    op.create_table(
        "word_examples",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("word_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("korean_sentence", sa.Text(), nullable=False),
        sa.Column("chinese_translation", sa.Text(), nullable=True),
        sa.Column("source_type", sa.String(30), nullable=True),
        sa.Column("source_name", sa.String(200), nullable=True),
        sa.Column("source_date", sa.Date(), nullable=True),
        sa.Column("pronunciation_audio_url", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"]),
    )

    # ### word_progress ###
    op.create_table(
        "word_progress",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("word_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("learned", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("review_count", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("last_review_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("next_review_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("srs_interval_days", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("consecutive_correct", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("learning_stage", sa.String(10), nullable=False, server_default="new"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
        sa.ForeignKeyConstraint(["word_id"], ["words.id"]),
    )

    # ### grammar_points ###
    op.create_table(
        "grammar_points",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("title", sa.String(200), nullable=True),
        sa.Column("level", sa.Integer(), nullable=True),
        sa.Column("structure_formula", sa.Text(), nullable=True),
        sa.Column("explanation", sa.Text(), nullable=True),
        sa.Column("usage_scenario", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # ### grammar_examples ###
    op.create_table(
        "grammar_examples",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("grammar_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("korean_sentence", sa.Text(), nullable=True),
        sa.Column("chinese_translation", sa.Text(), nullable=True),
        sa.Column("is_wrong_example", sa.Boolean(), nullable=False, server_default="false"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["grammar_id"], ["grammar_points.id"]),
    )

    # ### batchim_rules ###
    op.create_table(
        "batchim_rules",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rule_type", sa.String(30), nullable=True),
        sa.Column("title", sa.String(200), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("animation_url", sa.Text(), nullable=True),
        sa.Column("order_index", sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )

    # ### batchim_examples ###
    op.create_table(
        "batchim_examples",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("rule_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("written_form", sa.String(200), nullable=True),
        sa.Column("pronounced_form", sa.String(200), nullable=True),
        sa.Column("process_description", sa.Text(), nullable=True),
        sa.Column("audio_url", sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["rule_id"], ["batchim_rules.id"]),
    )

    # ### daily_tasks ###
    op.create_table(
        "daily_tasks",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column(
            "task_date",
            sa.Date(),
            nullable=False,
            server_default=sa.func.current_date(),
        ),
        sa.Column("words_completed", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("grammar_completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("listening_completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.Column("speaking_completed", sa.Boolean(), nullable=False, server_default="false"),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    # ### activity_log ###
    op.create_table(
        "activity_log",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("activity_type", sa.String(30), nullable=True),
        sa.Column("target_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("score", sa.Float(), nullable=True),
        sa.Column("xp_earned", sa.Integer(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    # ### user_badges ###
    op.create_table(
        "user_badges",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("badge_type", sa.String(50), nullable=True),
        sa.Column(
            "earned_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )

    # ### chat_history ###
    op.create_table(
        "chat_history",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("role", sa.String(10), nullable=True),
        sa.Column("content", sa.Text(), nullable=True),
        sa.Column("context_type", sa.String(30), nullable=True),
        sa.Column("scenario_name", sa.String(100), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"]),
    )


def downgrade() -> None:
    op.drop_table("chat_history")
    op.drop_table("user_badges")
    op.drop_table("activity_log")
    op.drop_table("daily_tasks")
    op.drop_table("batchim_examples")
    op.drop_table("batchim_rules")
    op.drop_table("grammar_examples")
    op.drop_table("grammar_points")
    op.drop_table("word_progress")
    op.drop_table("word_examples")
    op.drop_table("words")
    op.drop_table("letter_progress")
    op.drop_table("letters")
    op.drop_table("user_progress")
    op.drop_table("users")
