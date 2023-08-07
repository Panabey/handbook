"""Initial

Revision ID: 974c9216dae1
Revises:
Create Date: 2023-08-07 06:59:55.065162

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "974c9216dae1"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "posts",
        sa.Column("anons", sa.String(length=255), nullable=False, server_default=""),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("posts", "anons")
    # ### end Alembic commands ###
