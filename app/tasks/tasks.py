import smtplib
from app.config import settings
from app.tasks.celery_app import celery
from app.tasks.email_templates import create_order_confirmation_template


@celery.task
def send_email_report_dashboard(order: dict):
    """ Отправка письма пользователю
    """
    email = create_order_confirmation_template(order)

    with smtplib.SMTP_SSL(settings.SMTP_HOST, settings.SMTP_PORT) as server:
        server.login(settings.SMTP_USER, settings.SMTP_PASS)
        server.send_message(email)
