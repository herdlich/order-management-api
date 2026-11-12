from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.api.dependencies import get_product_service, get_current_user
from app.exceptions.base import ProductAlreadyExistsError, UnknownProductCreateError, NoPermissionError
from app.features.products.schemas import ProductCreate, ProductResponse
from app.features.products.services import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, summary="Create Product")
async def create_product_endpoint(data: ProductCreate, service: Annotated[ProductService, Depends(get_product_service)],
                                  current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        return await service.product_create(data, current_user.user_id)

    except ProductAlreadyExistsError:
        raise HTTPException(
            status_code=409,
            detail="Product with this name already exists",
        )

    except UnknownProductCreateError:
        raise HTTPException(
            status_code=404,
            detail="Unknown product error"
        )

    except NoPermissionError:
        raise HTTPException(
            status_code=403,
            detail="You don't have permission to perform this action"
        )