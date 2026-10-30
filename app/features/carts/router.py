from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_cart_item_service,
    get_cart_service,
    get_current_user,
)
from app.features.cart_items.schemas import CartItemCreate, CartItemResponse
from app.features.cart_items.services import CartItemService
from app.features.carts.services import CartService

router = APIRouter(prefix="/carts", tags=["Carts"])


@router.post("/my/items", response_model=CartItemResponse)
async def add_product_to_cart_endpoint(data: CartItemCreate,
                                       cart_item_service: Annotated[CartItemService, Depends(get_cart_item_service)],
                                       cart_service: Annotated[CartService, Depends(get_cart_service)],
                                       current_user: Annotated[dict, Depends(get_current_user)]):
    user_id = current_user.user_id

    return await cart_item_service.cart_item_create(data, user_id)
