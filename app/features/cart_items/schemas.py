from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int = Field(gt=0, description="The quantity must be greater than 0")


class CartItemDelete(BaseModel):
    cart_item_id: int
    quantity: int


class CartItemResponse(SchemaBase):
    cart_item_id: int
    product_id: int
    quantity: int
    created_at: datetime