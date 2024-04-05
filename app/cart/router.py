from fastapi import APIRouter, Request, status

from app.cart.service import CartService


router_cart = APIRouter(
    prefix="/cart",
    tags=["Корзина"]
)


@router_cart.post("/add-to-cart/{product_id}", status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(
            request: Request,
            product_id: int,
            quantity: int = 1,
            override_quantity: bool = False
):
    """ Добавление или обновление товаров в корзине
    """
    return await CartService.service_add_product_to_cart(request, product_id, quantity, override_quantity)


@router_cart.get("/get-product-cart")
async def get_products_in_cart(request: Request):
    """ Получение корзины
    """
    return await CartService.service_get_products_in_cart(request)


@router_cart.delete("/delete_from_cart/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_product_from_cart(
            request: Request,
            product_id: int
):
    """ Удаление товаров из корзины
    """
    return await CartService.service_remove_product_from_cart(request, product_id)


@router_cart.get("/get_total_quantity")
async def get_total_quantity_in_cart(request: Request):
    """ Общее количество товаров в корзине
    """
    return await CartService.service_get_total_quantity_in_cart(request)


@router_cart.get("/get_total_price")
async def get_total_price_in_cart(request: Request):
    """ Суммарная стоимость всех товаров в корзине
    """
    return await CartService.service_get_total_price_in_cart(request)
