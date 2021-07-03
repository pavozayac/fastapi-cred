import datetime
from .db.database import Base
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator, ValidationError

class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    phone: str
    
    @validator('phone')
    def validate_phone(cls, v: str):
        if not v.isnumeric() or ' ' in v or len(v) != 9:
            raise ValidationError('Invalid phone number')
 
class UserIn(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    is_verified: bool

class LoginSchema(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    token: str
    expires_at: datetime.datetime