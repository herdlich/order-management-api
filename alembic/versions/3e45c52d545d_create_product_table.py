from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

revision: str = '3e45c52d545d'
down_revision: Union[str, Sequence[str], None] = '683534623d38'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('products',
    sa.Column('product_id', sa.Integer(), nullable=False),
    sa.Column('product_name', sa.String(), nullable=False),
    sa.Column('product_cost', sa.Numeric(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.CheckConstraint('product_cost > 0', name='check_cost_positive'),
    sa.PrimaryKeyConstraint('product_id')
    )


def downgrade() -> None:
    op.drop_table('products')
