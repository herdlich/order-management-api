from sqlalchemy.ext.asyncio import AsyncSession
from app.features.cart_items.schemas import CartItemCreate
from app.features.cart_items.models import CartItem


class CartItemDatabase:
    @staticmethod
    async def add_cart_item(session: AsyncSession, cart_item_model: CartItemCreate, cart_id: int) -> CartItemCreate:
        cart_item = CartItem(
            cart_id=cart_id,
            product_id=cart_item_model.product_id,
            quantity=cart_item_model.quantity,
        )

        session.add(cart_item)
        await session.commit()
        await session.refresh(cart_item_model)

        return cart_item_model