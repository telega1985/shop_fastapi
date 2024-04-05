from app.orders.models import created_at
from app.products.models import intpk
from app.database import Base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship


class Coupon(Base):
    """ Модель купонов на скидку
    """
    __tablename__ = "coupon"

    id: Mapped[intpk]
    code: Mapped[str] = mapped_column(unique=True)
    valid_from: Mapped[created_at]
    valid_to: Mapped[created_at]
    discount: Mapped[int]
    active: Mapped[bool] = mapped_column(server_default="t")
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    orders: Mapped[list["Order"]] = relationship(back_populates="coupon")
    user: Mapped["User"] = relationship(back_populates="coupons")

    def __str__(self) -> str:
        return self.code
