from pydantic import BaseModel
from typing import Optional

class Ad(BaseModel):
    title: str
    content: str
    price: Optional[float] = None
    phone: Optional[str] = None
    category: str

class UpdateAd(Ad):
    bolha_id: str

class User(BaseModel):
    user_name: str
    bolha_password: str