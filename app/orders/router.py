from fastapi import APIRouter, Request, status
from app.orders.schemas import SOrderCreate, SOrderInfo
from app.orders.service import OrderService

router_order = APIRouter(
    prefix="/orders",
    tags=["Заказы"]
)


@router_order.post("", status_code=status.HTTP_201_CREATED)
async def create_new_order(request: Request, order: SOrderCreate):
    return await OrderService.service_create_new_order(request, order)


@router_order.get("")
async def get_last_order_for_frontend() -> SOrderInfo:
    return await OrderService.service_get_last_order_for_frontend()
