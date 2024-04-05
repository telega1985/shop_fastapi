from email.message import EmailMessage
from app.config import settings


def create_order_confirmation_template(order: dict):
    """ Создание письма для подтверждения заказа
    """
    email = EmailMessage()

    email["Subject"] = "Подтверждение заказа"
    email["From"] = settings.SMTP_USER
    email["To"] = order["email"]

    email.set_content(
        f"""
        <h1>Подтвердите заказ номер {order["id"]}</h1>
        <p>Дорогой {order["first_name"]}</p>
        <p>Вы подтвердили заказ на оплату</p>
        <p>Ваш номер заказа {order["id"]}</p>
        """,
        subtype="html"
    )

    return email
