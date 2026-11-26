from collections.abc import Sequence

from sqlalchemy import delete, select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import CartItemNotFoundError
from app.features.cart_items.models import CartItem
from app.features.carts.models import Cart


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
    async def list_cart_items(session: AsyncSession, *, cart_id: int) -> Sequence[CartItem] | None:
        stmt = select(CartItem).where(CartItem.cart_id == cart_id)
        result = await session.scalars(stmt)

        return result

    @staticmethod
    async def clear_cart_items_by_cart_id(session: AsyncSession, cart_id: int) -> None:
        stmt = delete(CartItem).where(CartItem.cart_id == cart_id)
        await session.execute(stmt)

    @staticmethod
    async def delete_cart_item_by_its_id(session: AsyncSession, user_id: int, cart_item_id: int) -> None:
        stmt = (
            select(CartItem)
            .join(Cart)
            .where(
                CartItem.cart_item_id == cart_item_id,
                Cart.user_id == user_id,
            )
        )

        cart_item = await session.scalar(stmt)

        if not cart_item:
            raise CartItemNotFoundError

        await session.delete(cart_item)

    @staticmethod
    async def set_cart_item_quantity_by_its_id(
            session: AsyncSession,
            user_id: int,
            cart_item_id: int,
            quantity: int,
    ) -> None:
        stmt = (
            select(CartItem)
            .join(Cart)
            .where(
                CartItem.cart_item_id == cart_item_id,
                Cart.user_id == user_id,
            )
        )

        cart_item = await session.scalar(stmt)

        if not cart_item:
            raise CartItemNotFoundError

        cart_item.quantity = quantity

    @staticmethod
    async def get_cart_item_by_its_id(session: AsyncSession, cart_item_id: int) -> CartItem | None:
        result = await session.get(CartItem, cart_item_id)

        return result

    @staticmethod
    async def get_cart_item_by_cart_and_product_ids(session: AsyncSession, cart_id: int, product_id: int):
        stmt = select(CartItem).where(
            CartItem.cart_id == cart_id,
            CartItem.product_id == product_id,
        )
        result = await session.scalar(stmt)

        return result