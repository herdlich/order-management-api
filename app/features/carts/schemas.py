from datetime import datetime

from pydantic import BaseModel, ConfigDict


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    
class CartCreate(BaseModel):
    user_id: int


class CartResponse(SchemaBase):
    cart_id: int
    user_id: int
    created_at: datetime