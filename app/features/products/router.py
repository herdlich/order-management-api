from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status

from app.api.dependencies import get_current_user, get_product_service
from app.exceptions.base import (
    NonExistentPageError,
    NoPermissionError,
    PageSizeMustBeGreaterThanZeroError,
    ProductAlreadyArchivedError,
    ProductAlreadyExistsError,
    ProductNotFoundError,
    ProductNotInArchiveError,
    UnknownProductCreateError,
)
from app.features.products.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.features.products.services import ProductService

router = APIRouter(prefix="/products", tags=["Products"])


@router.post("", response_model=ProductResponse, summary="Create Product")
async def create_product_endpoint(data: ProductCreate, service: Annotated[ProductService, Depends(get_product_service)],
                                  current_user: Annotated[dict, Depends(get_current_user)]):
    try:
        return await service.create_product(data, current_user.user_id)

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


@router.get("/page/{page_number}", response_model=list[ProductResponse], summary="Get All Products")
async def get_all_products_on_the_page_endpoint(
        page_number: int,
        service: Annotated[ProductService, Depends(get_product_service)],
):
    try:
        return await service.list_products(page_number)

    except NonExistentPageError:
        raise HTTPException(
            status_code=404,
            detail="Page with this number does not exist"
        )

    except PageSizeMustBeGreaterThanZeroError:
        raise HTTPException(
            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load the list of products; please try again later",
        )


@router.get("/{product_id}", response_model=ProductResponse, summary="Get Product")
async def get_product_by_id_endpoint(
        product_id: int,
        service: Annotated[ProductService, Depends(get_product_service)],
):
    try:
        return await service.get_product_by_id(product_id)

    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product with this id does not exist"
        )


@router.patch("/{product_id}", response_model=ProductResponse, summary="Update Product")
async def update_product_endpoint(
        product_id: int,
        data: ProductUpdate,
        service: Annotated[ProductService, Depends(get_product_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    try:
        return await service.update_product(product_id, data, current_user.user_id)

    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product with this id does not exist"
        )


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete Product")
async def archive_product_endpoint(
        product_id: int,
        service: Annotated[ProductService, Depends(get_product_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    try:
        await service.archive_product(current_user.user_id, product_id)

        return

    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product with this id does not exist"
        )

    except ProductAlreadyArchivedError:
        raise HTTPException(
            status_code=409,
            detail="This product is already archived",
        )


@router.patch("/{product_id}/unarchive", status_code=status.HTTP_204_NO_CONTENT, summary="Unarchive Product")
async def unarchive_product_endpoint(
        product_id: int,
        service: Annotated[ProductService, Depends(get_product_service)],
        current_user: Annotated[dict, Depends(get_current_user)],
):
    try:
        return await service.unarchive_product(current_user.user_id, product_id)

    except ProductNotFoundError:
        raise HTTPException(
            status_code=404,
            detail="Product with this id does not exist"
        )

    except ProductNotInArchiveError:
        raise HTTPException(
            status_code=409,
            detail="This product not archived",
        )
