from app.coupons.models import Coupon
from app.dao.base import BaseDAO


class CouponDAO(BaseDAO):
    model = Coupon
