from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_current_user, get_order_service
from app.features.orders.schemas import OrderResponse
from app.features.orders.services import OrderService
from app.exceptions.base import OrderNotFoundError

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, summary="Create Order")
async def create_order_endpoint(service: Annotated[OrderService, Depends(get_order_service)],
                                current_user: Annotated[dict, Depends(get_current_user)]) -> OrderResponse:
    return await service.create_order(current_user.user_id)


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
