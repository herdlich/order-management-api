"""add min_length validation for product_name

Revision ID: 4576cb377dac
Revises: 73d8a9c5e036
Create Date: 2026-11-18 05:19:51.353163

"""
from collections.abc import Sequence

from alembic import op

# revision identifiers, used by Alembic.
revision: str = '4576cb377dac'
down_revision: str | Sequence[str] | None = '73d8a9c5e036'
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    op.create_check_constraint(
        "check_product_name_min_length",
        "products",
        "length(trim(product_name)) >= 3",
    )


def downgrade() -> None:
    op.drop_constraint(
        "check_product_name_min_length",
        "products",
        type_="check",
    )
