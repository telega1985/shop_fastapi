import os
from typing import Optional

from fastapi import UploadFile, File, HTTPException
from app.database import async_session_maker
from app.reviews.dao import ReviewDAO, ImageReviewDAO
from app.reviews.schemas import SReviewCreate, SImageReviewInfo
from app.reviews.image_utils import image_add_origin

from app.logger import logger


class ReviewService:
    @classmethod
    async def service_upload_photo_for_review(cls, image: UploadFile = File(...)) -> SImageReviewInfo:
        path_folder = "app/static/review_images"

        if not os.path.exists(path_folder):
            os.mkdir(path_folder)

        path_file = await image_add_origin(path_folder, image)
        relative_path = f"/review_images/{path_file}"

        async with async_session_maker() as session:
            new_photo = await ImageReviewDAO.create(
                session,
                image=relative_path
            )
            await session.commit()

        return new_photo

    @classmethod
    async def service_get_photo_by_id(cls, image_id: Optional[int] = None):
        async with async_session_maker() as session:
            return await ImageReviewDAO.get_one(session, id=image_id)

    @classmethod
    async def service_create_new_review(cls, review: SReviewCreate):
        try:
            photo_id = None
            if review.image_id is not None:
                photo = await cls.service_get_photo_by_id(review.image_id)
                if photo:
                    photo_id = photo.id

            new_review_data = review.model_dump(exclude={"image_id", "parent_id"})

            async with async_session_maker() as session:
                new_review = await ReviewDAO.create(
                    session,
                    **new_review_data,
                    image_id=photo_id,
                    parent_id=review.parent_id or None
                )

                await session.commit()

            return new_review
        except Exception as e:
            msg = "An error add review"
            logger.error(msg, exc_info=True)
            raise HTTPException(status_code=500, detail="Internal Server Error")
