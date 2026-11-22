from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.features.orders.models import Order, OrderItem
from app.exceptions.base import OrderNotFoundError


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

    @staticmethod
    async def get_order_by_its_id(session: AsyncSession, user_id: int, order_id: int) -> Order | None:
        stmt = select(Order).where(
            Order.user_id == user_id,
            Order.order_id == order_id,
        )

        result = await session.scalar(stmt)

        if not result:
            raise OrderNotFoundError

        return result
