from app.products.models import intpk
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Optional


class ImageReview(Base):
    __tablename__ = "image_review"

    id: Mapped[intpk]
    image: Mapped[Optional[str]]

    review: Mapped["Review"] = relationship(back_populates="image")

    def __str__(self) -> str:
        return self.image


class Review(Base):
    __tablename__ = "review"

    id: Mapped[intpk]
    parent_id: Mapped[Optional[int]] = mapped_column(ForeignKey("review.id", ondelete="SET NULL"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    name: Mapped[str]
    text: Mapped[str]
    image_id: Mapped[Optional[int]] = mapped_column(ForeignKey("image_review.id", ondelete="SET NULL"))

    product: Mapped["Products"] = relationship(back_populates="reviews")
    image: Mapped["ImageReview"] = relationship(back_populates="review")
    parent: Mapped["Review"] = relationship(remote_side="[Review.id]", back_populates="replies")
    replies: Mapped[list["Review"]] = relationship(remote_side="[Review.parent_id]", back_populates="parent")

    def __str__(self) -> str:
        return self.name
