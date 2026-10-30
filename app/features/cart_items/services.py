from sqlalchemy.ext.asyncio import AsyncSession

from app.features.cart_items.models import CartItem
from app.features.cart_items.repository import CartItemDatabase
from app.features.cart_items.schemas import CartItemCreate
from app.features.carts.repository import CartDatabase


class CartItemService:
    def __init__(self, session: AsyncSession, cart_item_repository: CartItemDatabase, cart_repository: CartDatabase):
        self.session = session
        self.cart_item_repository = cart_item_repository
        self.cart_repository = cart_repository

    async def cart_item_create(self, cart_item_model: CartItemCreate, user_id: int) -> CartItem | None:
        try:
            cart = await self.cart_repository.get_cart_by_user_id(self.session, user_id)

            if cart is None:
                cart = await self.cart_repository.create_cart(self.session, user_id)

            cart_item_model_to_db = CartItem(
                cart_id=cart.cart_id,
                product_id=cart_item_model.product_id,
                quantity=cart_item_model.quantity,
            )

            created_cart_item = await self.cart_item_repository.add_or_increment(self.session, cart_item_model_to_db)

            self.session.add(created_cart_item)

            await self.session.commit()
            await self.session.refresh(created_cart_item)

            return created_cart_item

        except Exception:
            await self.session.rollback()
            raise
