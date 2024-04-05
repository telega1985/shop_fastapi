from fastapi import Request

from app.cart.redis_utils import RedisTools
from app.database import async_session_maker
from app.logger import logger
from decimal import Decimal
from app.products.dao import ProductsDAO
from app.recommender.service import RecommenderService


class CartService:
    @classmethod
    async def service_add_product_to_cart(
            cls,
            request: Request,
            product_id: int,
            quantity: int = 1,
            override_quantity: bool = False
    ):
        session_id, cart = await RedisTools.get_cart_with_session_id(request)

        async with async_session_maker() as session:
            product = await ProductsDAO.get_one(session, id=product_id)

            product_id = str(product.id)

            if product_id not in cart:
                cart[product_id] = {"quantity": 0, "price": str(product.price)}

            if override_quantity:
                cart[product_id]["quantity"] = quantity
            else:
                cart[product_id]["quantity"] += quantity

            await RedisTools.save_cart(session_id, cart)

            all_products = await ProductsDAO.get_bd_list_product(session)

        await RecommenderService.service_products_bought(all_products)

        return cart

    @classmethod
    async def service_get_products_in_cart(cls, request: Request):
        products = []
        try:
            session_id, cart = await RedisTools.get_cart_with_session_id(request)

            async with async_session_maker() as session:
                for product_id, product_info in cart.items():
                    if product_id.isdigit():
                        product = await ProductsDAO.get_bd_one_product_with_category_by_id(session, int(product_id))
                        if product:
                            product_info["product"] = product
                            product_info["price"] = Decimal(product_info["price"])
                            product_info["total_price"] = product_info["price"] * product_info["quantity"]
                            products.append(product_info)

                return products
        except Exception as e:
            msg = "An error occurred while processing products in cart"
            logger.error(msg, exc_info=True)
            return []

    @classmethod
    async def service_remove_product_from_cart(
            cls,
            request: Request,
            product_id: int
    ):
        session_id, cart = await RedisTools.get_cart_with_session_id(request)

        async with async_session_maker() as session:
            product = await ProductsDAO.get_one(session, id=product_id)

        product_id = str(product.id)

        if product_id in cart:
            del cart[product_id]
            await RedisTools.save_cart(session_id, cart)

        return {"message": "Product removed from cart"}

    @classmethod
    async def service_get_total_quantity_in_cart(cls, request: Request):
        session_id, cart = await RedisTools.get_cart_with_session_id(request)
        return sum(item["quantity"] for item in cart.values())

    @classmethod
    async def service_get_total_price_in_cart(cls, request: Request):
        session_id, cart = await RedisTools.get_cart_with_session_id(request)
        return sum(Decimal(item["price"]) * item["quantity"] for item in cart.values())
