from pydantic import BaseModel

from app.reviews.schemas import SReviewInfo


class SCategoriesInfo(BaseModel):
    name: str
    slug: str


class SProductInfo(BaseModel):
    id: int
    name: str
    slug: str
    price: float
    image: str


class SProductsWithCategoriesInfo(SProductInfo):
    category: SCategoriesInfo


class SProductsWithCategoriesAndReviewsInfo(SProductsWithCategoriesInfo):
    reviews: list[SReviewInfo]


class SCategoryWithProductsInfo(SCategoriesInfo):
    products: list[SProductInfo]
