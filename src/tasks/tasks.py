import smtplib
from email.message import EmailMessage

from loguru import logger
from pydantic import EmailStr

from config import settings
from src.tasks.celery_app import celery
from src.tasks.email_templates import create_booking_confirmation_template


@celery.task
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    msg_content: EmailMessage = create_booking_confirmation_template(booking, email_to)

    with smtplib.SMTP_SSL(settings.smtp_host, settings.smtp_port) as server:
        server.login(settings.smtp_user, settings.smtp_password)
        server.send_message(msg_content)
    logger.info(f"Successfully send email message to {email_to}")
