from pydantic import BaseModel, EmailStr
from typing import Optional


class SOrderCreate(BaseModel):
    coupon_id: Optional[int]
    first_name: str
    last_name: str
    email: EmailStr
    address: str
    city: str


class SOrderInfo(SOrderCreate):
    id: int
