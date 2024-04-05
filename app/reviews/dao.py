from app.reviews.models import Review, ImageReview
from app.dao.base import BaseDAO


class ReviewDAO(BaseDAO):
    model = Review


class ImageReviewDAO(BaseDAO):
    model = ImageReview
