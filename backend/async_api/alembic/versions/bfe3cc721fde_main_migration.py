"""main migration

Revision ID: bfe3cc721fde
Revises:
Create Date: 2023-10-13 16:24:03.323077

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "bfe3cc721fde"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "article",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("title", sa.String(length=120), nullable=False),
        sa.Column("anons", sa.String(length=400), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("update_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("create_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("reading_time", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_article_id"), "article", ["id"], unique=False)
    op.create_table(
        "handbook_category",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "handbook_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=40), nullable=False),
        sa.Column("color_text", sa.String(length=7), nullable=False),
        sa.Column("color_background", sa.String(length=7), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "project_news",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("reading_time", sa.Integer(), nullable=False),
        sa.Column("create_date", sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "quiz_topic",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "tag_status",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=60), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "handbook",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.Column("description", sa.String(length=300), nullable=True),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("is_visible", sa.Boolean(), nullable=False),
        sa.Column("category_id", sa.Integer(), nullable=True),
        sa.Column("status_id", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["handbook_category.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.ForeignKeyConstraint(
            ["status_id"],
            ["handbook_status.id"],
            onupdate="CASCADE",
            ondelete="SET NULL",
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_table(
        "quiz",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("topic_id", sa.Integer(), nullable=True),
        sa.Column("logo_url", sa.String(), nullable=True),
        sa.Column("title", sa.String(length=100), nullable=False),
        sa.Column("short_description", sa.String(length=255), nullable=False),
        sa.Column("description", sa.String(length=500), nullable=False),
        sa.Column("is_visible", sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(
            ["topic_id"], ["quiz_topic.id"], onupdate="CASCADE", ondelete="SET NULL"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quiz_id"), "quiz", ["id"], unique=False)
    op.create_table(
        "tag",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("title", sa.String(length=60), nullable=False),
        sa.Column("status_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["status_id"], ["tag_status.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("title"),
    )
    op.create_index(op.f("ix_tag_id"), "tag", ["id"], unique=False)
    op.create_table(
        "article_tag",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("article_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["article_id"], ["article.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["tag.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "handbook_content",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("handbook_id", sa.Integer(), nullable=False),
        sa.Column("part", sa.SmallInteger(), nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.Column("description", sa.String(length=400), nullable=False),
        sa.ForeignKeyConstraint(
            ["handbook_id"], ["handbook.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_handbook_content_id"), "handbook_content", ["id"], unique=False
    )
    op.create_table(
        "quiz_question",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quiz_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=400), nullable=False),
        sa.Column("hint", sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(
            ["quiz_id"], ["quiz.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quiz_question_id"), "quiz_question", ["id"], unique=False)
    op.create_table(
        "quiz_tag",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("quiz_id", sa.Integer(), nullable=False),
        sa.Column("tag_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["quiz_id"], ["quiz.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["tag_id"], ["tag.id"], onupdate="CASCADE", ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "handbook_page",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("content_id", sa.Integer(), nullable=False),
        sa.Column("subpart", sa.SmallInteger(), nullable=False),
        sa.Column("title", sa.String(length=80), nullable=False),
        sa.Column("short_description", sa.String(length=255), nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("reading_time", sa.Integer(), nullable=False),
        sa.Column("update_date", sa.DateTime(timezone=True), nullable=False),
        sa.Column("create_date", sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(
            ["content_id"],
            ["handbook_content.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_handbook_page_id"), "handbook_page", ["id"], unique=False)
    op.create_table(
        "quiz_answer",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("question_id", sa.Integer(), nullable=False),
        sa.Column("text", sa.String(length=255), nullable=False),
        sa.Column("is_correct", sa.Boolean(), nullable=False),
        sa.Column("explanation", sa.String(length=300), nullable=True),
        sa.ForeignKeyConstraint(
            ["question_id"],
            ["quiz_question.id"],
            onupdate="CASCADE",
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_quiz_answer_id"), "quiz_answer", ["id"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f("ix_quiz_answer_id"), table_name="quiz_answer")
    op.drop_table("quiz_answer")
    op.drop_index(op.f("ix_handbook_page_id"), table_name="handbook_page")
    op.drop_table("handbook_page")
    op.drop_table("quiz_tag")
    op.drop_index(op.f("ix_quiz_question_id"), table_name="quiz_question")
    op.drop_table("quiz_question")
    op.drop_index(op.f("ix_handbook_content_id"), table_name="handbook_content")
    op.drop_table("handbook_content")
    op.drop_table("article_tag")
    op.drop_index(op.f("ix_tag_id"), table_name="tag")
    op.drop_table("tag")
    op.drop_index(op.f("ix_quiz_id"), table_name="quiz")
    op.drop_table("quiz")
    op.drop_table("handbook")
    op.drop_table("tag_status")
    op.drop_table("quiz_topic")
    op.drop_table("project_news")
    op.drop_table("handbook_status")
    op.drop_table("handbook_category")
    op.drop_index(op.f("ix_article_id"), table_name="article")
    op.drop_table("article")
    # ### end Alembic commands ###
