"""added status handbook

Revision ID: eacc48c5eb2a
Revises: f2d9e36c059e
Create Date: 2023-08-11 07:37:28.338404

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "eacc48c5eb2a"
down_revision = "f2d9e36c059e"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("handbook", sa.Column("status_id", sa.Integer(), nullable=True))
    op.create_foreign_key(
        None,
        "handbook",
        "status",
        ["status_id"],
        ["id"],
        onupdate="CASCADE",
        ondelete="SET NULL",
    )
    op.drop_column("handbook", "is_complemented")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "handbook",
        sa.Column("is_complemented", sa.BOOLEAN(), autoincrement=False, nullable=False),
    )
    op.drop_constraint(None, "handbook", type_="foreignkey")
    op.drop_column("handbook", "status_id")
    # ### end Alembic commands ###