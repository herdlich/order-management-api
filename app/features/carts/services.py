from sqlalchemy.ext.asyncio import AsyncSession

from app.features.carts.schemas import CartCreate
from app.features.carts.models import Cart
from app.features.carts.repository import CartDatabase


class CartService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_cart(self, cart_model: CartCreate):
        cart_data_to_db = Cart(
            user_id=cart_model.user_id,
        )

        created_cart = await CartDatabase.add_cart_to_db(self.session, cart_data_to_db)

        return created_cart