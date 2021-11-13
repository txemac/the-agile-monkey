"""table customer

Revision ID: 64341fbf7c32
Revises: 1553028c0be2
Create Date: 2021-11-12 11:58:47.381557

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = '64341fbf7c32'
down_revision = '1553028c0be2'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "customer",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("surname", sa.String(), nullable=False),
        sa.Column("photo_url", sa.String(), nullable=True),
        sa.Column("dt_created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("dt_deleted", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_customer_id"), "user", ["id"], unique=True)


def downgrade():
    op.drop_index(op.f("ix_customer_id"), table_name="customer")
    op.drop_table("customer")
