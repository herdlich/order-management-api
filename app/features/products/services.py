from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import UnknownProductCreateError
from app.features.products.models import Product
from app.features.products.repository import ProductDatabase
from app.features.products.schemas import ProductCreate


class ProductService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def product_create(self, product_model: ProductCreate):
        product_model_to_db = Product(
            product_name=product_model.product_name,
            product_cost=product_model.product_cost,

        )

        created_product = await ProductDatabase.add_product_to_db(self.session, product_model_to_db)

        if not created_product:
            raise UnknownProductCreateError

        return created_product