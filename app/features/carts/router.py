from typing import Annotated

from fastapi import APIRouter, Depends

from app.features.carts.services import CartService
from app.features.carts.schemas import CartResponse, CartCreate
from app.api.dependencies import get_cart_service

router = APIRouter(prefix="/carts", tags=["Carts"])

@router.post("/", response_model=CartResponse)
async def create_cart_endpoint(data: CartCreate, service: Annotated[CartService, Depends(get_cart_service)]):
    return await service.create_cart(data)