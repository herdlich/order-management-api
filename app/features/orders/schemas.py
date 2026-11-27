from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict

from app.features.orders.models import OrderItem


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrderResponse(SchemaBase):
    order_id: int
    user_id: int
    status: str
    total_amount: Decimal
    created_at: datetime


class OrderItemResponse(SchemaBase):
    order_item_id: int
    order_id: int
    product_id: int
    unit_price: Decimal
    quantity: int
    created_at: datetime


class OrderDetailResponse(OrderResponse):
    items: list[OrderItemResponse]