from sqlalchemy.ext.asyncio import AsyncSession
from app.features.carts.models import Cart
from sqlalchemy import select


class CartDatabase:
    @staticmethod
    async def add_cart_to_db(session: AsyncSession, cart_model: Cart):
        cart = Cart(
            user_id=cart_model.user_id,
        )

        session.add(cart)
        await session.commit()
        await session.refresh(cart)
        return cart

    @staticmethod
    async def get_cart_by_user_id(session: AsyncSession, user_id: int):
        statement = select(Cart).where(Cart.user_id == user_id)
        cart = await session.scalar(statement)

        return cart