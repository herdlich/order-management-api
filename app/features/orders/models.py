from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    status: Mapped[str] = mapped_column(String(20), default="pending")

    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
    )

    __table_args__ = (
        CheckConstraint(
            "order_cost > 0",
            name="ck_orders_total_amount",
        ),
    )
