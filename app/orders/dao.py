from app.orders.models import Order, OrderItem
from app.dao.base import BaseDAO


class OrderDAO(BaseDAO):
    model = Order


class OrderItemDAO(BaseDAO):
    model = OrderItem
