from app.features.cart_items.repository import CartItemDatabase
from app.features.cart_items.schemas import CartItemCreate
from app.features.cart_items.models import CartItem
from app.features.carts.repository import CartDatabase
from sqlalchemy.ext.asyncio import AsyncSession


class CartItemService:
    def __init__(self, session: AsyncSession, cart_item_repository: CartItemDatabase, cart_repository: CartDatabase):
        self.session = session
        self.cart_item_repository = cart_item_repository
        self.cart_repository = cart_repository

    async def cart_item_create(self, cart_item_model: CartItemCreate, user_id: int) -> CartItem:
        cart_from_repository = await self.cart_repository.get_cart_by_user_id(self.session, user_id)

        cart_item_model_to_db = CartItem(
            cart_id=cart_from_repository.cart_id,
            product_id=cart_item_model.product_id,
            quantity=cart_item_model.quantity,
        )

        created_cart_item = await self.cart_item_repository.add_cart_item_to_db(self.session, cart_item_model_to_db)

        return created_cart_item
