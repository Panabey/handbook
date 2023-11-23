"""added slug for handbook

Revision ID: c7cc4b4a08d6
Revises: 27d58c38f635
Create Date: 2023-11-21 18:43:33.324620

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text

# revision identifiers, used by Alembic.
revision = "c7cc4b4a08d6"
down_revision = "27d58c38f635"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("handbook", sa.Column("slug", sa.String(length=80), nullable=True))
    connection = op.get_bind()
    connection.execute(text("UPDATE handbook SET slug = lower(title)"))
    op.alter_column("handbook", "slug", nullable=False)
    op.create_unique_constraint("handbook_slug_key", "handbook", ["slug"])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("handbook_slug_key", "handbook", type_="unique")
    op.drop_column("handbook", "slug")
    # ### end Alembic commands ###
