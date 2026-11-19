from sqlalchemy.ext.asyncio import AsyncSession

from app.features.carts.models import Cart
from app.features.carts.repository import CartDatabase


class CartService:
    def __init__(self, session: AsyncSession, cart_repository: CartDatabase):
        self.session = session
        self.cart_repository = cart_repository

    async def create_cart_if_it_does_not_exist(self, user_id: int) -> None:
        await self.cart_repository.create_cart(self.session, user_id)
