from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import UnknownProductCreateError, NoPermissionError
from app.features.products.models import Product
from app.features.products.repository import ProductDatabase
from app.features.products.schemas import ProductCreate
from app.features.users.repository import UserDatabase


class ProductService:
    def __init__(self, session: AsyncSession, product_repository: ProductDatabase, user_repository: UserDatabase):
        self.session = session
        self.product_repository = product_repository
        self.user_repository = user_repository

    async def product_create(self, product_model: ProductCreate, user_id: int):
        if not await self.user_repository.check_is_admin(self.session, user_id):
            raise NoPermissionError

        product_model_to_db = Product(
            product_name=product_model.product_name,
            product_cost=product_model.product_cost,

        )

        created_product = await self.product_repository.add_product_to_db(self.session, product_model_to_db)

        if not created_product:
            raise UnknownProductCreateError

        return created_product