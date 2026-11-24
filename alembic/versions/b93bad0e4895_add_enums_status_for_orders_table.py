"""add enums status for orders table

Revision ID: b93bad0e4895
Revises: 7657478c3cbb
Create Date: 2026-11-24 07:17:47.671707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

order_status_enum = postgresql.ENUM(
    "PENDING", "PAYED", "CANCELLED", "COMPLETED", name='orderstatus'
)


# revision identifiers, used by Alembic.
revision: str = 'b93bad0e4895'
down_revision: Union[str, Sequence[str], None] = '7657478c3cbb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    order_status_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column("orders", "status", server_default=None)

    op.execute(
        'ALTER TABLE orders ALTER COLUMN status TYPE orderstatus USING'
        ' UPPER(status)::orderstatus'
    )

    op.alter_column("orders", "status", server_default=sa.text("'PENDING'"))


def downgrade() -> None:
    op.alter_column("orders", "status", server_default=None)

    op.execute(
        'ALTER TABLE orders ALTER COLUMN status TYPE VARCHAR(20) USING'
        ' status::text'
    )

    order_status_enum.drop(op.get_bind(), checkfirst=True)
