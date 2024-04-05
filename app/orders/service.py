from fastapi import Request

from app.cart.redis_utils import RedisTools
from app.database import async_session_maker
from app.orders.dao import OrderDAO, OrderItemDAO
from app.orders.schemas import SOrderCreate, SOrderInfo
from app.tasks.tasks import send_email_report_dashboard


class OrderService:
    @classmethod
    async def service_create_new_order(cls, request: Request, order: SOrderCreate):
        session_id, cart = await RedisTools.get_cart_with_session_id(request)

        async with async_session_maker() as session:
            new_order = await OrderDAO.create(
                session,
                **order.model_dump()
            )

            for product_id, product_info in cart.items():
                await OrderItemDAO.create(
                    session,
                    order_id=new_order.id,
                    product_id=int(product_id),
                    price=float(product_info["price"]),
                    quantity=product_info["quantity"]
                )

            await session.commit()

        await RedisTools.clear_cart(session_id)

        order_dict = {
            "id": new_order.id,
            "first_name": new_order.first_name,
            "email": new_order.email
        }

        send_email_report_dashboard.delay(order_dict)

        return order_dict

    @classmethod
    async def service_get_last_order_for_frontend(cls) -> SOrderInfo:
        async with async_session_maker() as session:
            return await OrderDAO.get_last(session)
