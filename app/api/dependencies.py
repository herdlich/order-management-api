from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_session
from app.features.cart_items.repository import CartItemDatabase
from app.features.cart_items.services import CartItemService
from app.features.carts.services import CartService
from app.features.products.services import ProductService
from app.features.users.services import UserService
from app.features.users.repository import UserDatabase
from app.features.products.repository import ProductDatabase
from app.features.carts.repository import CartDatabase
from app.security.jwt_tokens import oauth2_scheme


async def get_current_user(
        token: Annotated[str, Depends(oauth2_scheme)],
        session: Annotated[AsyncSession, Depends(get_session)],
        user_repository: Annotated[UserDatabase, Depends(UserDatabase)],
):
    service = UserService(session, user_repository)

    user = await service.get_user_by_token(token)

    return user


async def get_user_service(session: Annotated[AsyncSession, Depends(get_session)],
                           user_repository: Annotated[UserDatabase, Depends(UserDatabase)]) -> UserService:
    return UserService(session, user_repository)


async def get_product_service(session: Annotated[AsyncSession, Depends(get_session)],
                              product_repository: Annotated[
                                  ProductDatabase, Depends(ProductDatabase)]) -> ProductService:
    return ProductService(session, product_repository)


async def get_cart_service(session: Annotated[AsyncSession, Depends(get_session)],
                           cart_repository: Annotated[CartDatabase, Depends(CartDatabase)]) -> CartService:
    return CartService(session, cart_repository)


async def get_cart_item_service(session: Annotated[AsyncSession, Depends(get_session)],
                                cart_item_repository: Annotated[
                                    CartItemDatabase, Depends(CartItemDatabase)],
                                cart_repository: Annotated[CartDatabase, Depends(CartDatabase)]) -> CartItemService:
    return CartItemService(session, cart_item_repository, cart_repository)
