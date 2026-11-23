from pathlib import Path

ROOT_PATH = Path(__file__).parent.resolve().parents[2]

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)

    product_name: Mapped[str] = mapped_column(nullable=False)

    product_cost: Mapped[Decimal]

    quantity: Mapped[int] = mapped_column(nullable=False, default='1')

    status: Mapped[str] = mapped_column(nullable=False, default="in_stock")
    
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "product_cost > 0",
            name="check_cost_positive",
        ),
        CheckConstraint(
            "length(trim(product_name)) >= 3",
            name="check_product_name_min_length",
        ),
        CheckConstraint(
            "quantity >= 0",
            name="check_quantity_positive",
        ),
        CheckConstraint(
            "status IN ('in_stock', 'out_of_stock')",
            name="check_valid_product_status",
        )
    )