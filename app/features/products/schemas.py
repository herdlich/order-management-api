from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)


class ProductCreate(BaseModel):
    product_name: str
    product_cost: Decimal = Field(gt=0, description="The cost must be greater than zero")


class ProductUpdate(BaseModel):
    product_name: str | None = Field(default=None, min_length=3)
    product_cost: Decimal | None = None
    quantity: int | None = Field(default=None, ge=0)


class ProductResponse(SchemaBase):
    product_id: int
    product_name: str
    product_cost: Decimal
    quantity: int
    status: str
    created_at: datetime