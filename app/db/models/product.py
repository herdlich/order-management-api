from pathlib import Path

ROOT_PATH = Path(__file__).parent.resolve().parents[2]

from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Product(Base):
    __tablename__ = "products"

    product_id: Mapped[int] = mapped_column(primary_key=True)

    product_name: Mapped[str] = mapped_column(nullable=False)

    product_cost: Mapped[Decimal]
    
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    __table_args__ = (
        CheckConstraint(
            "product_cost > 0",
            name="check_cost_positive",
        ),
    )