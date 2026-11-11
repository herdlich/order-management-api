from typing import Annotated
from fastapi import APIRouter, Depends
from app.api.dependencies import get_order_service, get_current_user
from app.features.orders.schemas import OrderResponse
from app.features.orders.services import OrderService

router = APIRouter(prefix="/orders", tags=["Orders"])


@router.post("", response_model=OrderResponse, summary="Create Order")
async def create_order_endpoint(service: Annotated[OrderService, Depends(get_order_service)],
                                current_user: Annotated[dict, Depends(get_current_user)]) -> OrderResponse:
    return await service.create_order(current_user.user_id)
