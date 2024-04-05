from decimal import Decimal

from fastapi import APIRouter, Request

from app.coupons.schemas import SCouponInfo
from app.coupons.service import CouponService

router_coupon = APIRouter(
    prefix="/coupon",
    tags=["Купоны на скидку"]
)


@router_coupon.get("")
async def get_coupon_by_code(coupon_code: str) -> SCouponInfo:
    return await CouponService.service_get_coupon_by_code(coupon_code)


@router_coupon.get("/discount")
async def get_discount(request: Request, coupon_code: str) -> Decimal:
    return await CouponService.service_get_discount(request, coupon_code)


@router_coupon.get("/after-discount")
async def get_total_price_after_discount(request: Request, coupon_code: str):
    return await CouponService.service_get_total_price_after_discount(request, coupon_code)
