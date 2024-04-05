from pydantic import BaseModel
from typing import Optional


class SReviewCreate(BaseModel):
    product_id: int
    name: str
    text: str
    parent_id: Optional[int] = None
    image_id: Optional[int] = None


class SImageReviewInfo(BaseModel):
    id: int
    image: Optional[str]


class SReviewInfo(SReviewCreate):
    id: int
    image: Optional[SImageReviewInfo]
    replies: list["SReviewInfo"]
