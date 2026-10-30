from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.carts.models import Cart


class CartDatabase:
    @staticmethod
    async def create_cart(session: AsyncSession, user_id: int) -> Cart | None:
        cart = Cart(user_id=user_id)

        session.add(cart)
        await session.flush()

        return cart

    @staticmethod
    async def get_cart_by_user_id(session: AsyncSession, user_id: int):
        statement = select(Cart).where(Cart.user_id == user_id)
        cart = await session.scalar(statement)

        return cart