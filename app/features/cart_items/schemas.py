from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class CartItemCreate(BaseModel):
    product_id: int
    quantity: int


class CartItemDelete(BaseModel):
    cart_item_id: int
    quantity: int


class CartItemResponse(SchemaBase):
    cart_item_id: int
    product_id: int
    quantity: int
    created_at: datetime