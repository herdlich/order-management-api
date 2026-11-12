from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class OrderResponse(SchemaBase):
    order_id: int
    user_id: int
    status: str
    total_amount: Decimal
    created_at: datetime