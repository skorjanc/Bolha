from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    user_name: str
    password: str
    bolha_password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    user_name: str
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
    phone: Optional[str] = None 

class AdCreate(AdBase):
    pass

class AdUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    price: Optional[float] = None
    phone: Optional[str] = None 

class Ad(AdBase):
    id: int
    created_at: datetime
    published_at: datetime
    bolha_id: str

    class Config:
        orm_mode = True

class AdWithPublished(Ad):
    user: UserOut

class AdWithPosition(AdWithPublished):
    position: int

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None