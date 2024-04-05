from fastapi import APIRouter, UploadFile, File, status

from app.reviews.schemas import SReviewCreate, SImageReviewInfo
from app.reviews.service import ReviewService

router_review = APIRouter(
    prefix="/review",
    tags=["Отзывы"]
)


@router_review.post("", status_code=status.HTTP_201_CREATED)
async def create_new_review(review: SReviewCreate):
    return await ReviewService.service_create_new_review(review)


@router_review.post("/photo", status_code=status.HTTP_201_CREATED)
async def upload_photo_for_review(image: UploadFile = File(...)) -> SImageReviewInfo:
    return await ReviewService.service_upload_photo_for_review(image)
