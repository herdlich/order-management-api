from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import (
    get_cart_item_service,
    get_cart_service,
    get_current_user,
)
from app.features.cart_items.schemas import CartItemCreate, CartItemResponse, CartItemUpdate
from app.features.cart_items.services import CartItemService
from app.features.carts.services import CartService
from app.exceptions.base import CartItemNotFoundError, PermissibleQuantityExceededError

router = APIRouter(prefix="/carts", tags=["Carts"])


@router.post("/my/items", response_model=CartItemResponse)
async def add_product_to_cart_endpoint(data: CartItemCreate,
                                       cart_item_service: Annotated[CartItemService, Depends(get_cart_item_service)],
                                       current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        user_id = current_user.user_id

        return await cart_item_service.cart_item_create(data, user_id)

    except PermissibleQuantityExceededError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Quantity exceeded",
        )


@router.get("/my/items", response_model=list[CartItemResponse], summary="Get My Cart Items")
async def get_all_cart_items_endpoint(
        cart_service: Annotated[CartService, Depends(get_cart_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    return await cart_service.get_all_cart_items(current_user.user_id)


@router.delete("{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete My Cart Item")
async def delete_cart_item_endpoint(
        cart_item_id: int,
        cart_item_service: Annotated[CartItemService, Depends(get_cart_item_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    try:
        await cart_item_service.delete_cart_item(current_user.user_id, cart_item_id)

    except CartItemNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {cart_item_id} was not found in your cart",
        )


@router.patch("/{cart_item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def change_cart_item_quantity_endpoint(
        cart_item_id: int,
        data: CartItemUpdate,
        service: Annotated[CartItemService, Depends(get_cart_item_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    try:
        await service.change_cart_item_quantity(current_user.user_id, cart_item_id, data.quantity)

    except CartItemNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Item with id {cart_item_id} was not found in your cart",
        )
