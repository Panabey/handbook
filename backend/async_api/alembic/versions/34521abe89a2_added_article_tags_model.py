"""added article tags model

Revision ID: 34521abe89a2
Revises: 470d9cbf9f21
Create Date: 2023-08-22 13:50:40.891227

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "34521abe89a2"
down_revision = "470d9cbf9f21"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
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
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("article_tag")
    # ### end Alembic commands ###
