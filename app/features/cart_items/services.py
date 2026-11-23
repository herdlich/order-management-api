from sqlalchemy.ext.asyncio import AsyncSession

from app.features.cart_items.models import CartItem
from app.features.cart_items.repository import CartItemDatabase
from app.features.cart_items.schemas import CartItemCreate
from app.features.carts.repository import CartDatabase
from app.features.products.repository import ProductDatabase
from app.exceptions.base import PermissibleQuantityExceededError, CartItemNotFoundError


class CartItemService:
    def __init__(self, session: AsyncSession, cart_item_repository: CartItemDatabase, cart_repository: CartDatabase,
                 product_repository: ProductDatabase):
        self.session = session
        self.cart_item_repository = cart_item_repository
        self.cart_repository = cart_repository
        self.product_repository = product_repository

    async def cart_item_create(self, cart_item_model: CartItemCreate, user_id: int) -> CartItem | None:
        try:
            cart = await self.cart_repository.get_cart_by_user_id(self.session, user_id)

            if cart is None:
                cart = await self.cart_repository.create_cart(self.session, user_id)

            product = await self.product_repository.get_product_by_id(self.session, cart_item_model.product_id)

            if product.quantity < cart_item_model.quantity:
                raise PermissibleQuantityExceededError

            update_product_quantity = product.quantity - cart_item_model.quantity

            cart_item_model_to_db = CartItem(
                cart_id=cart.cart_id,
                product_id=cart_item_model.product_id,
                quantity=cart_item_model.quantity,
            )

            await self.product_repository.change_product_quantity(
                self.session,
                cart_item_model.product_id,
                update_product_quantity,
            )

            created_cart_item = await self.cart_item_repository.add_or_increment(self.session, cart_item_model_to_db)

            self.session.add(created_cart_item)

            await self.session.commit()
            await self.session.refresh(created_cart_item)

            return created_cart_item



        except Exception:
            await self.session.rollback()
            raise

    async def delete_cart_item(self, user_id, cart_item_id):
        await self.cart_item_repository.delete_cart_item_by_its_id(self.session, user_id, cart_item_id)

        await self.session.commit()

    async def change_cart_item_quantity(self, user_id: int, cart_item_id: int, quantity: int) -> None:
        cart_item = await self.cart_item_repository.get_cart_item_by_its_id(self.session, cart_item_id)

        if cart_item is None:
            raise CartItemNotFoundError

        product = await self.product_repository.get_product_by_id(self.session, cart_item.product_id)

        if product.quantity < quantity:
            raise PermissibleQuantityExceededError

        updated_quantity = product.quantity - quantity

        await self.cart_item_repository.change_cart_item_quantity_by_its_id(
            self.session,
            user_id,
            cart_item_id,
            quantity,
        )

        await self.product_repository.change_product_quantity(
            self.session,
            product.product_id,
            updated_quantity,
        )

        await self.session.commit()
