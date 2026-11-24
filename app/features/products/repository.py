import math

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import (
    NonExistentPageError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
)
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

    @staticmethod
    async def get_all_products_on_the_page_database(session: AsyncSession, *, page_size: int, page_number: int) -> list:
        if page_number < 1:
            raise NonExistentPageError

        if page_size < 1:
            print("page_size must be greater than 0")  # temporary replacement for logs
            raise

        count_stmt = select(func.count(Product.product_id))
        total_count = await session.scalar(count_stmt) or 0

        if total_count == 0 and page_number > 1:
            raise NonExistentPageError

        total_pages = math.ceil(total_count / page_size)

        if total_count > 0 and page_number > total_pages:
            raise NonExistentPageError

        offset = (page_number - 1) * page_size
        stmt = (
            select(*Product.__table__.c)
            .order_by(Product.product_id.asc())
            .offset(offset)
            .limit(page_size)
        )
        result = (await session.execute(stmt)).mappings().all()

        return list(result)

    @staticmethod
    async def get_product_by_id(session: AsyncSession, product_id: int) -> Product:
        result = await session.get(Product, product_id)

        if result is None:
            raise ProductNotFoundError

        # noinspection PyTypeChecker
        return result

    @staticmethod
    async def update_product_in_database(session: AsyncSession, product: Product) -> Product:
        await session.commit()
        await session.refresh(product)

        return product


    @staticmethod
    async def delete_product_from_database(session: AsyncSession, product_id: int) -> None:
        product = await session.get(Product, product_id)

        if product is None:
            raise ProductNotFoundError

        await session.delete(product)

    @staticmethod
    async def change_product_quantity(session: AsyncSession, product_id: int, quantity: int):
        if quantity < 0:
            raise ValueError("Quantity must be greater than 0")

        stmt = select(Product).where(Product.product_id == product_id)
        product = await session.scalar(stmt)

        if product is None:
            raise ProductNotFoundError

        product.quantity = quantity