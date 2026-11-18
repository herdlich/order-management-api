from sqlalchemy.ext.asyncio import AsyncSession

from app.exceptions.base import NoPermissionError, UnknownProductCreateError
from app.features.products.models import Product
from app.features.products.repository import ProductDatabase
from app.features.products.schemas import ProductCreate, ProductUpdate
from app.features.users.repository import UserDatabase

PAGE_SIZE = 10


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

    async def get_all_products_on_the_page(self, page_number: int) -> list[Product]:
        products = await self.product_repository.get_all_products_on_the_page_database(
            self.session,
            page_size=PAGE_SIZE,
            page_number=page_number,
        )

        return products

    async def get_product_by_id(self, product_id: int) -> Product:
        product = await self.product_repository.get_product_by_id(self.session, product_id)

        return product

    async def update_product(self, product_id: int, data: ProductUpdate):
        product = await self.product_repository.get_product_by_id(self.session, product_id)

        update_data = data.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(product, field, value)

        return await self.product_repository.update_product_in_database(self.session, product)