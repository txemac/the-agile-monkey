"""table user

Revision ID: 1553028c0be2
Revises:
Create Date: 2021-11-11 17:30:13.014315

"""
import sqlalchemy as sa
import sqlalchemy_utils
from alembic import op

# revision identifiers, used by Alembic.
revision = "1553028c0be2"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "user",
        sa.Column("id", sqlalchemy_utils.types.uuid.UUIDType(), nullable=False),
        sa.Column("username", sa.String(), nullable=False),
        sa.Column("password", sa.String(), nullable=False),
        sa.Column("dt_created", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("dt_deleted", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_admin", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id")
    )
    op.create_index(op.f("ix_user_id"), "user", ["id"], unique=True)
    op.create_index(op.f("ix_user_username"), "user", ["username"], unique=True)

    pg_connection = op.get_bind()
    pg_connection.execute(
        """
    insert into "user" (id, username, password, dt_created, dt_deleted, is_admin)
    values ('6fc330b1-3d65-402c-b7a3-b5b526240505', 'admin',
    '$2b$12$a/BvAPooibsSdwzkNUEjeOl7oOOdguqmoLogl9qRqTi9xsFCMKf5a', now(), null, true);
    """
    )


def downgrade():
    op.drop_index(op.f("ix_user_username"), table_name="user")
    op.drop_index(op.f("ix_user_id"), table_name="user")
    op.drop_table("user")
