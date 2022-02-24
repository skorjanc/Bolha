from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True

class UserUpdatePassword(BaseModel):
    id: int
    old_password: str
    new_password: str

class UserLogin(UserCreate):
    pass

class AdBase(BaseModel):
    title: str
    content: str
    category: str
    price: Optional[float] = None
    phone: Optional[int] = None 

class AdCreate(AdBase):
    pass

class AdUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    price: Optional[float] = None
    phone: Optional[int] = None 

class Ad(AdBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True

class AdWithPublished(Ad):
    published_at: Optional[datetime] = None
    user: UserOut


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None