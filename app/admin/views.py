from sqladmin import ModelView

from app.coupons.models import Coupon
from app.orders.models import Order, OrderItem
from app.products.models import Categories, Products
from app.reviews.models import Review, ImageReview
from app.users.models import User


class CategoriesAdmin(ModelView, model=Categories):
    column_list = [c.name for c in Categories.__table__.c] + [Categories.products, Categories.user]
    page_size = 20
    name = "Категория"
    name_plural = "Категории"
    icon = "fa-solid fa-table"


class ProductsAdmin(ModelView, model=Products):
    column_list = [c.name for c in Products.__table__.c] + [Products.category, Products.order, Products.user]
    page_size = 20
    name = "Товар"
    name_plural = "Товары"
    icon = "fa-brands fa-product-hunt"


class OrderAdmin(ModelView, model=Order):
    column_list = [c.name for c in Order.__table__.c] + [Order.coupon, Order.order_items]
    page_size = 20
    name = "Заказ"
    name_plural = "Заказы"
    icon = "fa-brands fa-first-order"


class OrderItemAdmin(ModelView, model=OrderItem):
    column_list = [c.name for c in OrderItem.__table__.c] + [OrderItem.products, OrderItem.order]
    page_size = 20
    name = "Приобретенный товар"
    name_plural = "Приобретенные товары"
    icon = "fa-brands fa-first-order-alt"


class CouponAdmin(ModelView, model=Coupon):
    column_list = [c.name for c in Coupon.__table__.c] + [Coupon.orders, Coupon.user]
    page_size = 20
    name = "Купон"
    name_plural = "Купоны"
    icon = "fa-solid fa-ticket"


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.username, User.categories, User.products, User.coupons]
    column_details_exclude_list = [User.hashed_password]
    can_delete = False
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"


class ReviewAdmin(ModelView, model=Review):
    column_list = [c.name for c in Review.__table__.c] + [Review.product, Review.image, Review.parent, Review.replies]
    page_size = 20
    name = "Отзыв"
    name_plural = "Отзывы"
    icon = "fa-solid fa-comment"


class ReviewImageAdmin(ModelView, model=ImageReview):
    column_list = [c.name for c in ImageReview.__table__.c] + [ImageReview.review]
    page_size = 20
    name = "Фотография"
    name_plural = "Фотографии"
    icon = "fa-solid fa-camera"
