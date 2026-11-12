from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.features.cart_items.models import CartItem


class CartItemDatabase:
    @staticmethod
    async def add_or_increment(session: AsyncSession, cart_item_model: CartItem) -> CartItem | None:
        stmt = insert(CartItem).values(
            cart_id=cart_item_model.cart_id,
            product_id=cart_item_model.product_id,
            quantity=cart_item_model.quantity,
        )

        stmt = stmt.on_conflict_do_update(
            constraint="uq_cart_product",
            set_={
                "quantity": (
                    CartItem.quantity + stmt.excluded.quantity
                ),
            },
        ).returning(CartItem)

        result = await session.scalar(stmt)

        if result is None:
            raise RuntimeError("Cart item was not returned")

        return result



    @staticmethod
    async def get_all_cart_items_by_cart_id(session: AsyncSession, cart_id: int) -> Sequence[CartItem] | None:
        stmt = select(CartItem).where(CartItem.cart_id == cart_id)
        result = await session.scalars(stmt)

        return result.all()

    @staticmethod
    async def clear_cart_items_by_cart_id(session: AsyncSession, cart_id: int) -> None:
        stmt = delete(CartItem).where(CartItem.cart_id == cart_id)
        await session.execute(stmt)
