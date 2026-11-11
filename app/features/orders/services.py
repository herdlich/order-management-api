from app.features.orders.models import Order, OrderItem
from app.features.orders.repository import OrderDatabase
from app.features.products.repository import ProductDatabase
from app.features.carts.repository import CartDatabase
from app.features.cart_items.repository import CartItemDatabase


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

            cart_items_with_cost = await self.product_repository.get_products_by_cart_id(self.session, user_cart.cart_id)

            total_amount = sum(
                cost * item.quantity
                for item, cost in cart_items_with_cost
            )

            order_data_to_db = Order(
                user_id=user_id,
                total_amount=total_amount
            )

            order = await self.order_repository.add_order(self.session, order_data_to_db)

            # --------------------------------------------------------------------------------
            # order_item create

            order_items = []

            for item, cost in cart_items_with_cost:
                order_item = OrderItem(
                    order_id=order.order_id,
                    product_id=item.product_id,
                    unit_price=cost,
                    quantity=item.quantity,
                )

                order_items.append(order_item)

            await self.order_repository.add_all_order_items(self.session, order_items)

            await self.cart_item_repository.clear_cart_items_by_cart_id(self.session, user_cart.cart_id)

            await self.session.commit()

            return order

        except Exception:
            await self.session.rollback()


