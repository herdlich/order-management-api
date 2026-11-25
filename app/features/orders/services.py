from app.enums import OrderStatus, ProductStatus
from app.exceptions.base import (
    CartIsEmptyError,
    InvalidOrderStatusTransitionError,
    OrderAlreadyCancelledError,
    OrderCantBeCancelledError,
    OrderNotFoundError,
    PermissibleQuantityExceededError,
    ProductNotFoundError,
)
from app.features.cart_items.repository import CartItemDatabase
from app.features.carts.repository import CartDatabase
from app.features.orders.models import Order, OrderItem
from app.features.orders.repository import OrderDatabase
from app.features.products.repository import ProductDatabase


class OrderService:
    def __init__(self, session, order_repository: OrderDatabase, cart_repository: CartDatabase,
                 cart_item_repository: CartItemDatabase,
                 product_repository: ProductDatabase):
        self.session = session
        self.order_repository = order_repository
        self.cart_repository = cart_repository
        self.cart_item_repository = cart_item_repository
        self.product_repository = product_repository

    async def create_order(self, user_id):
        try:
            # order create
            user_cart = await self.cart_repository.get_cart_by_user_id(self.session, user_id)

            if user_cart is None:
                raise CartIsEmptyError

            cart_items_with_products = await self.product_repository.get_products_by_cart_id(self.session,
                                                                                         user_cart.cart_id)

            total_amount = sum(
                product.product_cost * item.quantity
                for item, product in cart_items_with_products
            )

            if total_amount <= 0:
                raise CartIsEmptyError

            order_data_to_db = Order(
                user_id=user_id,
                total_amount=total_amount
            )

            order = await self.order_repository.add_order(self.session, order_data_to_db)

            # --------------------------------------------------------------------------------
            # order_item create

            order_items = []

            for item, product in cart_items_with_products:
                if product is None:
                    raise ProductNotFoundError

                if product.status == ProductStatus.ARCHIVED:
                    raise ProductNotFoundError

                if product.quantity < item.quantity:
                    raise PermissibleQuantityExceededError

                product.quantity -= item.quantity

                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=item.product_id,
                    unit_price=product.product_cost,
                    quantity=item.quantity,
                )

                order_items.append(order_item)

            await self.order_repository.add_all_order_items(self.session, order_items)

            await self.cart_item_repository.clear_cart_items_by_cart_id(self.session, user_cart.cart_id)

            await self.session.commit()

            await self.session.refresh(order)

            return order

        except Exception:
            await self.session.rollback()
            raise

    async def get_order(self, user_id: int, order_id: int):
        order = await self.order_repository.get_order_by_its_id(self.session, user_id, order_id)

        return order

    async def get_all_orders(self, user_id: int):
        orders = await self.order_repository.get_all_orders_by_user_id(self.session, user_id)

        return orders

    async def cancel_order(self, user_id: int, order_id: int):
        try:
            order = await self.order_repository.get_order_by_its_id(self.session, user_id, order_id)

            if order is None:
                raise OrderNotFoundError

            if order.status == OrderStatus.CANCELLED:
                raise OrderAlreadyCancelledError

            if order.status == OrderStatus.COMPLETED:
                raise OrderCantBeCancelledError

            order.status = OrderStatus.CANCELLED

            order_items = await self.order_repository.get_all_order_items_by_order_id(
                self.session,
                order_id,
            )

            for item in order_items:
                product = await self.product_repository.get_product_by_id(self.session, item.product_id)

                if product is not None:
                    product.quantity += item.quantity

            await self.session.commit()
            await self.session.refresh(order)

            return order

        except Exception:
            await self.session.rollback()

            raise

    async def pay_order(self, user_id: int, order_id: int):
        order = await self.order_repository.get_order_by_its_id(self.session, user_id, order_id)

        if order is None:
            raise OrderNotFoundError

        if order.status != OrderStatus.PENDING:
            raise InvalidOrderStatusTransitionError

        order.status = OrderStatus.PAYED

        await self.session.commit()
        await self.session.refresh(order)
        return order
