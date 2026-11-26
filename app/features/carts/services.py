from sqlalchemy.ext.asyncio import AsyncSession

from app.features.cart_items.repository import CartItemDatabase
from app.features.carts.repository import CartDatabase


class CartService:
    def __init__(self, session: AsyncSession, cart_repository: CartDatabase, cart_item_repository: CartItemDatabase):
        self.session = session
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository

    async def create_cart_if_it_does_not_exist(self, user_id: int) -> None:
        await self.cart_repository.create_cart(self.session, user_id)

    async def get_all_cart_items(self, user_id: int):
        cart = await self.cart_repository.get_cart_by_user_id(self.session, user_id)
        cart_items = await self.cart_item_repository.list_cart_items(self.session, cart_id=cart.cart_id)
        return cart_items
