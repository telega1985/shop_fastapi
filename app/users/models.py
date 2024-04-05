from app.database import Base
from sqlalchemy.orm import Mapped, relationship

from app.products.models import intpk


class User(Base):
    __tablename__ = "user"

    id: Mapped[intpk]
    username: Mapped[str]
    hashed_password: Mapped[str]

    categories: Mapped[list["Categories"]] = relationship(back_populates="user")
    products: Mapped[list["Products"]] = relationship(back_populates="user")
    coupons: Mapped[list["Coupon"]] = relationship(back_populates="user")

    def __str__(self):
        return f"Пользователь {self.username}"
