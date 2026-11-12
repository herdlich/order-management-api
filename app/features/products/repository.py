from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import ProductAlreadyExistsError
from app.features.cart_items.models import CartItem
from app.features.products.models import Product


class ProductDatabase:
    @staticmethod
    async def add_product_to_db(session: AsyncSession, product_model: Product):
        try:
            statement_check_product = select(Product).where(Product.product_name == product_model.product_name)
            check_product_name_exists = await session.scalar(statement_check_product)

            if check_product_name_exists is not None:
                raise ProductAlreadyExistsError

            session.add(product_model)
            await session.commit()
            await session.refresh(product_model)

            return product_model

        except Exception as e:
            await session.rollback()
            raise e

    @staticmethod
    async def get_products_by_cart_id(session: AsyncSession, cart_id: int):
        stmt = (
            select(CartItem, Product.product_cost)
            .join(Product, CartItem.product_id == Product.product_id)
            .where(CartItem.cart_id == cart_id)
        )

        products = await session.execute(stmt)

        return products.all()
