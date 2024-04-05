from app.cart.redis_utils import redis_connect
from app.database import async_session_maker
from app.products.dao import ProductsDAO
from app.products.schemas import SProductsWithCategoriesInfo


class RecommenderService:
    @classmethod
    async def service_get_product_key(cls, product_id: int):
        return f"product:{product_id}:purchased_with"

    @classmethod
    async def service_products_bought(cls, products: list[SProductsWithCategoriesInfo]):
        product_ids = [p.id for p in products]
        product_keys = [await cls.service_get_product_key(product_id) for product_id in product_ids]

        for product_key in product_keys:
            for with_id in product_ids:
                if with_id != product_key:
                    await redis_connect.zincrby(product_key, 1, with_id)

    @classmethod
    async def service_suggest_products_for(
            cls, products: list[SProductsWithCategoriesInfo], max_results: int = 6
    ) -> list[SProductsWithCategoriesInfo]:
        product_ids = [p.id for p in products]

        if len(products) == 1:
            suggestions = await redis_connect.zrange(
                await cls.service_get_product_key(product_ids[0]), 0, -1, desc=True
            )
        else:
            flat_ids = "".join(str(product_id) for product_id in product_ids)
            tmp_key = f"tmp_{flat_ids}"
            product_keys = [await cls.service_get_product_key(product_id) for product_id in product_ids]

            await redis_connect.zunionstore(tmp_key, product_keys)
            suggestions = await redis_connect.zrange(tmp_key, 0, -1, desc=True)
            await redis_connect.delete(tmp_key)

        suggested_products_ids = [int(product_id) for product_id in suggestions]

        suggested_products_ids = [pid for pid in suggested_products_ids if pid not in product_ids]

        async with async_session_maker() as session:
            suggested_products = await ProductsDAO.get_bd_one_product_with_category_in(
                session,
                suggested_products_ids
            )
        suggested_products.sort(key=lambda x: suggested_products_ids.index(x.id))

        return suggested_products[:max_results]

    @classmethod
    async def service_clear_purchases(cls):
        async with async_session_maker() as session:
            product_ids = await ProductsDAO.get_all(session)
        all_product_keys = [await cls.service_get_product_key(product.id) for product in product_ids]
        await redis_connect.delete(*all_product_keys)
