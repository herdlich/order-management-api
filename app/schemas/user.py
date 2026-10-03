from pydantic import BaseModel, ConfigDict, EmailStr


class SchemaBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str