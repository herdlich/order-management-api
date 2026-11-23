from pathlib import Path

ROOT_PATH = Path(__file__).parent.resolve().parents[2]

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from app.db.base import Base
from app.enums import ProductStatus


class Product(Base):
    __tablename__ = "products"

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
            "status IN ('IN_STOCK', 'OUT_OF_STOCK', 'ARCHIVED')",
            name="check_valid_product_status",
        )
    )

    product_id: Mapped[int] = mapped_column(primary_key=True)

    product_name: Mapped[str] = mapped_column(nullable=False)

    product_cost: Mapped[Decimal]

    quantity: Mapped[int] = mapped_column(nullable=False, default=0)

    status: Mapped[ProductStatus] = mapped_column(
        nullable=False,
        default=ProductStatus.OUT_OF_STOCK,
        server_default=ProductStatus.OUT_OF_STOCK,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    @validates("quantity")
    def validate_quantity(self, key, new_quantity):
        if new_quantity < 0:
            raise ValueError("Quantity must be >= 0")

        if self.status != ProductStatus.ARCHIVED:
            self.status = (
                ProductStatus.IN_STOCK if new_quantity > 0
                else ProductStatus.OUT_OF_STOCK
            )

        return new_quantity
