"""relationships at customer table

Revision ID: 883aada49f94
Revises: 64341fbf7c32
Create Date: 2021-11-13 12:40:03.119819

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = '883aada49f94'
down_revision = '64341fbf7c32'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column("user", sa.Column("dt_updated", sa.DateTime(timezone=True), nullable=True))
    op.add_column("customer", sa.Column("dt_updated", sa.DateTime(timezone=True), nullable=True))
    op.add_column("customer", sa.Column("created_by_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False))
    op.add_column("customer", sa.Column("updated_by_id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=True))


def downgrade():
    op.drop_column("customer", "updated_by_id")
    op.drop_column("customer", "created_by_id")
    op.drop_column("customer", "dt_updated")
    op.drop_column("user", "dt_updated")
