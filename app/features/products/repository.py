from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import ProductAlreadyExistsError
from app.features.products.models import Product
from app.features.products.schemas import ProductCreate


class ProductDatabase:
    @staticmethod
    async def add_product_to_db(session: AsyncSession, product_model: ProductCreate):
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