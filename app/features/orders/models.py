from datetime import datetime
from decimal import Decimal

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Numeric, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.enums import OrderStatus


class Order(Base):
    __tablename__ = "orders"

    order_id: Mapped[int] = mapped_column(primary_key=True)

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))

    status: Mapped[OrderStatus] = mapped_column(
        nullable=False,
        default=OrderStatus.PENDING,
        server_default=OrderStatus.PENDING,
    )

    total_amount: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    items: Mapped[list["OrderItem"]] = relationship(
        back_populates="order",
    )

    __table_args__ = (
        CheckConstraint(
            "total_amount > 0",
            name="ck_orders_total_amount",
        ),
        CheckConstraint(
            "status IN ('PENDING', 'PAYED', 'CANCELLED', 'COMPLETED')",
            name="check_valid_order_status",
        )
    )


class OrderItem(Base):
    __tablename__ = "order_items"

    order_item_id: Mapped[int] = mapped_column(primary_key=True)

    order_id: Mapped[int] = mapped_column(ForeignKey("orders.order_id"))

    product_id: Mapped[int] = mapped_column(ForeignKey("products.product_id"))

    unit_price: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    quantity: Mapped[int] = mapped_column()

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    order: Mapped["Order"] = relationship(
        back_populates="items",
    )

    __table_args__ = (
        CheckConstraint(
            "quantity > 0",
            name="ck_order_items_quantity",
        ),
    )
