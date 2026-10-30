from sqlalchemy.ext.asyncio import AsyncSession

from app.features.carts.models import Cart
from app.features.carts.repository import CartDatabase


class CartService:
    def __init__(self, session: AsyncSession, cart_repository: CartDatabase):
        self.session = session
        self.cart_repository = cart_repository

    async def create_cart_if_it_does_not_exist(self, user_id: int) -> None:
        cart_data_to_db = Cart(
            user_id=user_id,
        )

        await self.cart_repository.add_cart_to_db_if_it_does_not_exist(self.session, cart_data_to_db, user_id)
