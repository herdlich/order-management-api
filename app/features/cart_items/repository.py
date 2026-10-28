from sqlalchemy.ext.asyncio import AsyncSession
from app.features.cart_items.models import CartItem


class CartItemDatabase:
    @staticmethod
    async def add_cart_item_to_db(session: AsyncSession, cart_item_model: CartItem) -> CartItem:
        session.add(cart_item_model)
        await session.commit()
        await session.refresh(cart_item_model)

        return cart_item_model