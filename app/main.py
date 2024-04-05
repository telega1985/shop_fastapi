from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi_versioning import VersionedFastAPI
from sqladmin import Admin
from fastapi.responses import RedirectResponse

from app.admin.auth import authentication_backend
from app.cart.redis_utils import RedisTools
from app.cart.router import router_cart
from app.coupons.router import router_coupon
from app.database import engine
from app.admin.views import (
    CategoriesAdmin,
    ProductsAdmin,
    OrderAdmin,
    OrderItemAdmin,
    CouponAdmin,
    UserAdmin,
    ReviewAdmin, ReviewImageAdmin
)
from app.orders.router import router_order
from app.products.router import router_products
from app.pages.router import router_frontend
from app.reviews.router import router_review
from app.users.router import router_auth

app = FastAPI(title="Internet shop")


# Основные роутеры

app.include_router(router_products)
app.include_router(router_cart)
app.include_router(router_order)
app.include_router(router_coupon)
app.include_router(router_auth)
app.include_router(router_review)


# Роутер для фронтенда

app.include_router(router_frontend)


# Версионирование API

app = VersionedFastAPI(
    app,
    version_format="{major}",
    prefix_format="/api/v{major}"
)


# Доступы для фронтенда для взаимодействия с нашим api

origins = [
    "http://localhost:8000",
    "http://localhost:7777"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type", "Set-Cookie",
        "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
        "Authorization"
    ]
)


# Админка

admin = Admin(app, engine, authentication_backend=authentication_backend)

admin.add_view(CategoriesAdmin)
admin.add_view(ProductsAdmin)
admin.add_view(OrderAdmin)
admin.add_view(OrderItemAdmin)
admin.add_view(CouponAdmin)
admin.add_view(ReviewAdmin)
admin.add_view(UserAdmin)
admin.add_view(ReviewImageAdmin)

# Путь к папке static (frontend)

app.mount("/static", StaticFiles(directory="app/static"), "static")


# Cookies для корзины

@app.middleware("http")
async def add_session_id(request: Request, call_next):
    response = await call_next(request)
    session_id = await RedisTools.get_session_id(request)
    response.set_cookie(key="session_id", value=str(session_id), httponly=True)

    # Страница 404

    if response.status_code == 404 or response.status_code == 500:
        return RedirectResponse("/api/v1/pages/not-found")

    return response
