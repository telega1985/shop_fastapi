from datetime import datetime, UTC
from app.products.models import intpk
from app.database import Base
from sqlalchemy import ForeignKey, text
from typing import Annotated
from sqlalchemy.orm import Mapped, mapped_column, relationship

created_at = Annotated[datetime, mapped_column(server_default=text("TIMEZONE('utc', now())"))]
updated_at = Annotated[datetime, mapped_column(
    server_default=text("TIMEZONE('utc', now())"), onupdate=datetime.now(UTC)
)]


class Order(Base):
    """ Детальная информация о заказе
    """
    __tablename__ = "order"

    id: Mapped[intpk]
    coupon_id: Mapped[int] = mapped_column(ForeignKey("coupon.id", ondelete="SET NULL"), nullable=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str]
    address: Mapped[str]
    city: Mapped[str]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]
    paid: Mapped[bool] = mapped_column(server_default="f")

    coupon: Mapped["Coupon"] = relationship(back_populates="orders")
    order_items: Mapped[list["OrderItem"]] = relationship(back_populates="order")

    def __str__(self) -> str:
        return f"Заказ {self.id}"


class OrderItem(Base):
    """ Приобретенный товар
    """
    __tablename__ = "order_item"

    id: Mapped[intpk]
    order_id: Mapped[int] = mapped_column(ForeignKey("order.id", ondelete="CASCADE"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id", ondelete="CASCADE"))
    price: Mapped[float]
    quantity: Mapped[int]

    products: Mapped["Products"] = relationship(back_populates="order")
    order: Mapped["Order"] = relationship(back_populates="order_items")

    def __str__(self) -> str:
        return str(self.id)
