"""add color field

Revision ID: c0ba7dfa9f7e
Revises: 1ea31af743ad
Create Date: 2023-09-02 16:42:44.772816

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "c0ba7dfa9f7e"
down_revision = "1ea31af743ad"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "status",
        sa.Column(
            "color_text", sa.String(length=7), nullable=False, server_default="#5573f3"
        ),
    )
    op.add_column(
        "status",
        sa.Column(
            "color_background",
            sa.String(length=7),
            nullable=False,
            server_default="#e2e8ff",
        ),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("status", "color_background")
    op.drop_column("status", "color_text")
    # ### end Alembic commands ###
