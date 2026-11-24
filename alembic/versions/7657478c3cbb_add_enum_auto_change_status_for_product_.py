"""add enum auto-change status for product table

Revision ID: 7657478c3cbb
Revises: 78001ede7b35
Create Date: 2026-11-23 12:18:29.549725

"""
from collections.abc import Sequence

import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '7657478c3cbb'
down_revision: str | Sequence[str] | None = '78001ede7b35'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

product_status_enum = postgresql.ENUM(
    'IN_STOCK', 'OUT_OF_STOCK', 'ARCHIVED', name='productstatus'
)


def upgrade() -> None:
    product_status_enum.create(op.get_bind(), checkfirst=True)

    op.alter_column('products', 'status', server_default=None)

    op.execute(
        'ALTER TABLE products ALTER COLUMN status TYPE productstatus USING'
        ' UPPER(status)::productstatus'
    )

    op.alter_column(
        'products', 'status', server_default=sa.text("'OUT_OF_STOCK'")
    )


def downgrade() -> None:
    op.alter_column('products', 'status', server_default=None)
    op.execute(
        'ALTER TABLE products ALTER COLUMN status TYPE VARCHAR USING status::text'
    )
    op.alter_column(
        'products', 'status', server_default=sa.text("'in_stock'")
    )

    product_status_enum.drop(op.get_bind(), checkfirst=True)
