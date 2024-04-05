from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from app.cart.router import get_products_in_cart, get_total_price_in_cart, get_total_quantity_in_cart
from app.coupons.router import get_coupon_by_code, get_discount, get_total_price_after_discount
from app.orders.router import get_last_order_for_frontend
from app.products.router import (
    get_all_category,
    get_all_products,
    get_category_with_product,
    get_one_product_with_category_and_reviews,
    get_list_product_by_name
)
from app.recommender.service import RecommenderService

router_frontend = APIRouter(
    prefix="/pages",
    tags=["Фронтенд"]
)

templates = Jinja2Templates(directory="app/templates")


@router_frontend.get("", response_class=HTMLResponse)
async def get_home_page(
        request: Request,
        products=Depends(get_all_products),
        categories=Depends(get_all_category),
        get_total_quantity=Depends(get_total_quantity_in_cart),
        get_total_price=Depends(get_total_price_in_cart)
):
    return templates.TemplateResponse(
        "product/product_list.html",
        {
            "request": request,
            "products": products,
            "categories": categories,
            "get_total_quantity": get_total_quantity,
            "get_total_price": get_total_price,
            "title": "Все товары"
        }
    )


@router_frontend.get("/not-found", response_class=HTMLResponse)
async def get_not_found_page(
        request: Request,
        get_total_quantity=Depends(get_total_quantity_in_cart),
        get_total_price=Depends(get_total_price_in_cart)
):
    return templates.TemplateResponse(
        "not_found_404/not_found_detail.html",
        {
            "request": request,
            "get_total_quantity": get_total_quantity,
            "get_total_price": get_total_price,
            "title": "Not found 404"
        }
    )


@router_frontend.get("/cart", response_class=HTMLResponse)
async def get_cart_detail_page(
        request: Request,
        cart=Depends(get_products_in_cart),
        get_total_price=Depends(get_total_price_in_cart),
        get_total_quantity=Depends(get_total_quantity_in_cart)
):
    cart_products = [item["product"] for item in cart]

    if cart_products:
        recommended_products = await RecommenderService.service_suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []

    return templates.TemplateResponse(
        "cart/cart_detail.html",
        {
            "request": request,
            "cart": cart,
            "get_total_price": get_total_price,
            "get_total_quantity": get_total_quantity,
            "recommended_products": recommended_products,
            "title": "Корзина"
        }
    )


@router_frontend.get("/order-create", response_class=HTMLResponse)
async def get_order_create_page(
        request: Request,
        cart=Depends(get_products_in_cart),
        get_total_price=Depends(get_total_price_in_cart),
        get_total_quantity=Depends(get_total_quantity_in_cart)
):
    return templates.TemplateResponse(
        "order/order_create.html",
        {
            "request": request,
            "cart": cart,
            "get_total_price": get_total_price,
            "get_total_quantity": get_total_quantity,
            "title": "Checkout"
        }
    )


@router_frontend.get("/order-created", response_class=HTMLResponse)
async def get_order_created_page(
        request: Request,
        order=Depends(get_last_order_for_frontend),
        get_total_price=Depends(get_total_price_in_cart),
        get_total_quantity=Depends(get_total_quantity_in_cart)
):
    return templates.TemplateResponse(
        "order/order_created.html",
        {
            "request": request,
            "order": order,
            "get_total_price": get_total_price,
            "get_total_quantity": get_total_quantity,
            "title": "Thank You"
        }
    )


@router_frontend.get("/{category_slug}", response_class=HTMLResponse)
async def get_product_in_category_page(
        request: Request,
        category_slug: str,
        category_by_slug_with_products=Depends(get_category_with_product),
        categories=Depends(get_all_category),
        get_total_price=Depends(get_total_price_in_cart),
        get_total_quantity=Depends(get_total_quantity_in_cart)
):
    return templates.TemplateResponse(
        "product/product_list.html",
        {
            "request": request,
            "category_slug": category_slug,
            "category_by_slug_with_products": category_by_slug_with_products.products,
            "categories": categories,
            "get_total_price": get_total_price,
            "get_total_quantity": get_total_quantity,
            "title": category_by_slug_with_products.name
        }
    )


@router_frontend.get("/cart/{coupon_code}", response_class=HTMLResponse)
async def get_coupon_in_cart_detail_page(
        request: Request,
        coupon=Depends(get_coupon_by_code),
        cart=Depends(get_products_in_cart),
        general_discount=Depends(get_discount),
        after_discount=Depends(get_total_price_after_discount),
        get_total_price=Depends(get_total_price_in_cart),
        get_total_quantity=Depends(get_total_quantity_in_cart)
):
    cart_products = [item["product"] for item in cart]

    if cart_products:
        recommended_products = await RecommenderService.service_suggest_products_for(cart_products, max_results=4)
    else:
        recommended_products = []

    return templates.TemplateResponse(
        "cart/cart_detail.html",
        {
            "request": request,
            "cart": cart,
            "coupon": coupon,
            "general_discount": general_discount,
            "after_discount": after_discount,
            "get_total_price": get_total_price,
            "recommended_products": recommended_products,
            "get_total_quantity": get_total_quantity,
            "title": coupon.code
        }
    )


@router_frontend.get("/not-found/{name}", response_class=HTMLResponse)
async def get_not_found_page(
        request: Request,
        name: str,
        product_by_name=Depends(get_list_product_by_name),
        get_total_quantity=Depends(get_total_quantity_in_cart),
        get_total_price=Depends(get_total_price_in_cart)
):
    return templates.TemplateResponse(
        "not_found_404/not_found_detail.html",
        {
            "request": request,
            "name": name,
            "product_by_name": product_by_name,
            "get_total_quantity": get_total_quantity,
            "get_total_price": get_total_price,
            "title": "Not found 404"
        }
    )


@router_frontend.get("/order-create/{coupon_code}", response_class=HTMLResponse)
async def get_coupon_in_order_create_page(
        request: Request,
        coupon=Depends(get_coupon_by_code),
        general_discount=Depends(get_discount),
        after_discount=Depends(get_total_price_after_discount),
        cart=Depends(get_products_in_cart),
        get_total_price=Depends(get_total_price_in_cart),
        get_total_quantity=Depends(get_total_quantity_in_cart)
):
    return templates.TemplateResponse(
        "order/order_create.html",
        {
            "request": request,
            "cart": cart,
            "coupon": coupon,
            "general_discount": general_discount,
            "after_discount": after_discount,
            "get_total_price": get_total_price,
            "get_total_quantity": get_total_quantity,
            "title": "Checkout"
        }
    )


@router_frontend.get("/{category_slug}/{product_slug}", response_class=HTMLResponse)
async def get_detail_product_page(
        request: Request,
        category_slug: str,
        product=Depends(get_one_product_with_category_and_reviews),
        get_total_price=Depends(get_total_price_in_cart),
        get_total_quantity=Depends(get_total_quantity_in_cart)
):
    recommended_products = await RecommenderService.service_suggest_products_for([product], max_results=4)

    return templates.TemplateResponse(
        "product/product_detail.html",
        {
            "request": request,
            "category_slug": category_slug,
            "product": product,
            "get_total_price": get_total_price,
            "get_total_quantity": get_total_quantity,
            "reviews": product.reviews,
            "recommended_products": recommended_products,
            "title": product.name
        }
    )
