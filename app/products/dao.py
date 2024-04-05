from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.dao.base import BaseDAO
from app.products.models import Products, Categories
from app.reviews.models import Review


class ProductsDAO(BaseDAO):
    model = Products

    @classmethod
    async def get_bd_list_product(cls, session: AsyncSession, limit: Optional[int] = None):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.category))
            .limit(limit).order_by(-cls.model.id.desc())
            .filter_by(available=True)
        )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_bd_list_product_by_name(cls, session: AsyncSession, name: str):
        category = await CategoriesDAO.get_one(session, name=name.capitalize())
        if category:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.category))
                .where(cls.model.category == category)
            )
        else:
            query = (
                select(cls.model)
                .options(selectinload(cls.model.category))
                .where(cls.model.name.ilike(f"%{name}%"))
            )
        result = await session.execute(query)
        return result.scalars().all()

    @classmethod
    async def get_bd_one_product_with_category_and_reviews(
            cls, session: AsyncSession, category_slug: str, product_slug: str
    ):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.category))
            .options(
                selectinload(cls.model.reviews)
                .options(selectinload(Review.image))
                .options(selectinload(Review.replies))
            )
            .join(cls.model.category)
            .where(Categories.slug == category_slug, cls.model.slug == product_slug)
        )
        result = await session.execute(query)
        product = result.scalars().one_or_none()

        if product:
            product.reviews = [review for review in product.reviews if review.parent_id is None]

        return product

    @classmethod
    async def get_bd_one_product_with_category_by_id(cls, session: AsyncSession, product_id: int):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.category))
            .filter_by(id=product_id)
        )
        result = await session.execute(query)
        return result.scalars().one_or_none()

    @classmethod
    async def get_bd_one_product_with_category_in(cls, session: AsyncSession, suggested_products_ids: list):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.category))
            .where(cls.model.id.in_(suggested_products_ids))
        )
        result = await session.execute(query)
        return result.scalars().all()


class CategoriesDAO(BaseDAO):
    model = Categories

    @classmethod
    async def get_category_bd_with_product(cls, session: AsyncSession, category_slug: str):
        query = (
            select(cls.model)
            .options(selectinload(cls.model.products))
            .filter_by(slug=category_slug)
        )
        result = await session.execute(query)
        category = result.scalars().one_or_none()

        if category:
            available_products = [product for product in category.products if product.available]
            category.products = available_products

        return category
