from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import date
from typing import Optional

class ContactBase(BaseModel):
    first_name: str = Field(max_length=50)
    last_name: str = Field(max_length=50)
    email: EmailStr
    phone: str = Field(max_length=20)
    birthday: date
    additional_data: Optional[str] = Field(None, max_length=250)

class ContactCreate(ContactBase):
    pass

class ContactUpdate(ContactBase):
    pass

class ContactResponse(ContactBase):
    id: int
   
    model_config = ConfigDict(from_attributes=True)