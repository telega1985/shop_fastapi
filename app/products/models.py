from app.database import Base
from sqlalchemy import ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.utils import CustomFileType

from typing import Annotated


intpk = Annotated[int, mapped_column(primary_key=True, index=True)]


class Categories(Base):
    __tablename__ = "categories"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(unique=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    products: Mapped[list["Products"]] = relationship(back_populates="category")
    user: Mapped["User"] = relationship(back_populates="categories")

    def __str__(self) -> str:
        return self.name


class Products(Base):
    __tablename__ = "products"

    id: Mapped[intpk]
    name: Mapped[str] = mapped_column(unique=True)
    slug: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str]
    price: Mapped[float]
    vendor_code: Mapped[str]
    available: Mapped[bool] = mapped_column(server_default="t")
    image = Column(CustomFileType())
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id", ondelete="CASCADE"))
    user_id: Mapped[int] = mapped_column(ForeignKey("user.id", ondelete="CASCADE"))

    category: Mapped["Categories"] = relationship(back_populates="products")
    order: Mapped[list["OrderItem"]] = relationship(back_populates="products")
    user: Mapped["User"] = relationship(back_populates="products")
    reviews: Mapped[list["Review"]] = relationship(back_populates="product")

    def __str__(self) -> str:
        return self.name
