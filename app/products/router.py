from typing import Optional

from fastapi import APIRouter

from app.products.schemas import (
    SCategoriesInfo,
    SProductsWithCategoriesInfo,
    SCategoryWithProductsInfo,
    SProductsWithCategoriesAndReviewsInfo
)
from app.products.service import ProductsService


router_products = APIRouter(
    prefix="/products",
    tags=["Товары"]
)


@router_products.get("/category")
async def get_all_category(limit: Optional[int] = None) -> list[SCategoriesInfo]:
    return await ProductsService.service_get_all_category(limit)


@router_products.get("")
async def get_all_products(limit: Optional[int] = None) -> list[SProductsWithCategoriesInfo]:
    return await ProductsService.service_get_all_products(limit)


@router_products.get("/{category_slug}")
async def get_category_with_product(category_slug: str) -> SCategoryWithProductsInfo:
    return await ProductsService.service_get_category_with_product(category_slug)


@router_products.get("/search-product/{name}")
async def get_list_product_by_name(name: str) -> list[SProductsWithCategoriesInfo]:
    return await ProductsService.service_get_list_product_by_name(name)


@router_products.get("/{category_slug}/{product_slug}")
async def get_one_product_with_category_and_reviews(
        category_slug: str,
        product_slug: str
) -> SProductsWithCategoriesAndReviewsInfo:
    return await ProductsService.service_get_one_product_with_category_and_reviews(category_slug, product_slug)
