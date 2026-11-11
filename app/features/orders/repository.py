from sqlalchemy.ext.asyncio import AsyncSession
from app.features.orders.models import Order, OrderItem


class OrderDatabase:
    @staticmethod
    async def add_order(session: AsyncSession, order_model: Order) -> Order:
        session.add(order_model)

        await session.flush()
        await session.refresh(order_model)

        return order_model

    @staticmethod
    async def add_all_order_items(session: AsyncSession, order_items: list[OrderItem]) -> None:
        session.add_all(order_items)

        await session.flush()
