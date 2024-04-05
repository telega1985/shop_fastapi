from typing import Optional

from app.database import async_session_maker
from app.products.dao import CategoriesDAO, ProductsDAO
from app.products.schemas import (
    SCategoriesInfo,
    SProductsWithCategoriesInfo,
    SCategoryWithProductsInfo,
    SProductsWithCategoriesAndReviewsInfo
)


class ProductsService:
    @classmethod
    async def service_get_all_category(cls, limit: Optional[int] = None) -> list[SCategoriesInfo]:
        async with async_session_maker() as session:
            return await CategoriesDAO.get_all(session, limit)

    @classmethod
    async def service_get_all_products(cls, limit: Optional[int] = None) -> list[SProductsWithCategoriesInfo]:
        async with async_session_maker() as session:
            return await ProductsDAO.get_bd_list_product(session, limit)

    @classmethod
    async def service_get_category_with_product(cls, category_slug: str) -> SCategoryWithProductsInfo:
        async with async_session_maker() as session:
            return await CategoriesDAO.get_category_bd_with_product(session, category_slug)

    @classmethod
    async def service_get_one_product_with_category_and_reviews(
            cls, category_slug: str,
            product_slug: str
    ) -> SProductsWithCategoriesAndReviewsInfo:
        async with async_session_maker() as session:
            return await ProductsDAO.get_bd_one_product_with_category_and_reviews(session, category_slug, product_slug)

    @classmethod
    async def service_get_list_product_by_name(cls, name: str) -> list[SProductsWithCategoriesInfo]:
        async with async_session_maker() as session:
            return await ProductsDAO.get_bd_list_product_by_name(session, name)
