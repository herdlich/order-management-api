from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user, get_order_service
from app.exceptions.base import (
    CartIsEmptyError,
    OrderAlreadyCancelledError,
    OrderCantBeCancelledError,
    OrderNotFoundError,
    PermissibleQuantityExceededError,
    ProductNotFoundError,
    InvalidOrderStatusTransitionError
)
from app.features.orders.schemas import OrderResponse
from app.features.orders.services import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, summary="Create Order")
async def create_order_endpoint(service: Annotated[OrderService, Depends(get_order_service)],
                                current_user: Annotated[dict, Depends(get_current_user)]) -> OrderResponse:
    try:
        return await service.create_order(current_user.user_id)

    except CartIsEmptyError:
        raise HTTPException(
            status_code=422,
            detail="Your cart is empty",
        )

    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product in your cart not found",
        )

    except PermissibleQuantityExceededError:
        raise HTTPException(
            status_code=422,
            detail="Quantity of the product in your cart exceeded",
        )


@router.get("/{order_id}", response_model=OrderResponse, summary="Get Order")
async def get_order_endpoint(
        order_id: int,
        service: Annotated[OrderService, Depends(get_order_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    try:
        return await service.get_order(current_user.user_id, order_id)

    except OrderNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Order with id {order_id} not found",
        )


@router.get("/", response_model=list[OrderResponse], summary="Get Orders")
async def get_all_orders_endpoint(
        service: Annotated[OrderService, Depends(get_order_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    return await service.get_all_orders(current_user.user_id)


@router.post("/{order_id}/cancel", response_model=OrderResponse, summary="Cancel Order")
async def cancel_order_endpoint(
        order_id: int,
        service: Annotated[OrderService, Depends(get_order_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    try:
        return await service.cancel_order(current_user.user_id, order_id)

    except OrderNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=f"Order with id {order_id} not found",
        )

    except OrderAlreadyCancelledError:
        raise HTTPException(
            status_code=422,
            detail=f"Order with id {order_id} already cancelled",
        )

    except OrderCantBeCancelledError:
        raise HTTPException(
            status_code=422,
            detail=f"Order with id {order_id} cant be cancelled",
        )


@router.post("/{order_id}/pay", response_model=OrderResponse, summary="Pay Order")
async def pay_order_endpoint(
        order_id: int,
        service: Annotated[OrderService, Depends(get_order_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    try:
        return await service.pay_order(current_user.user_id, order_id)

    except InvalidOrderStatusTransitionError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Invalid order state transition",
        )