from datetime import datetime
from decimal import Decimal
from fastapi import Request

from app.cart.service import CartService
from app.coupons.schemas import SCouponInfo
from app.database import async_session_maker
from app.coupons.dao import CouponDAO


class CouponService:
    @classmethod
    async def service_get_coupon_by_code(cls, coupon_code: str) -> SCouponInfo:
        async with async_session_maker() as session:
            return await CouponDAO.get_one(session, code=coupon_code)

    @staticmethod
    def service_coupon_is_valid(coupon: SCouponInfo) -> bool:
        current_time = datetime.now()
        return coupon.valid_from <= current_time <= coupon.valid_to and coupon.active

    @classmethod
    async def service_get_discount(cls, request: Request, coupon_code: str) -> Decimal:
        total_price = await CartService.service_get_total_price_in_cart(request)
        coupon = await cls.service_get_coupon_by_code(coupon_code)

        if coupon and cls.service_coupon_is_valid(coupon):
            return (coupon.discount / Decimal(100)) * total_price

        return Decimal(0)

    @classmethod
    async def service_get_total_price_after_discount(cls, request: Request, coupon_code: str):
        discount = await cls.service_get_discount(request, coupon_code)
        total_price = await CartService.service_get_total_price_in_cart(request)

        return total_price - discount
