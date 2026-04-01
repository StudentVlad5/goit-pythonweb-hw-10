from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime

class UserSchema(BaseModel):
    username: str = Field(min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(min_length=6, max_length=255)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: Optional[str]
    confirmed: bool = False
    created_at: datetime

    model_config = ConfigDict(from_attributes=True) # Дозволяє працювати з об'єктами SQLAlchemy

class TokenSchema(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RequestEmail(BaseModel):
    email: EmailStr