import asyncio

from fastapi_mail.errors import ConnectionErrors
from jinja2 import TemplateNotFound
from loguru import logger
from pydantic import EmailStr

from config import settings
from src.tasks.celery_app import celery
from src.tasks.mail import Mail


@celery.task(serializer="json")
def send_booking_confirmation_email(
    booking: dict,
    email_to: EmailStr,
):
    try:
        asyncio.run(
            Mail(
                url=settings.base_url,
                email=[email_to],
            ).create_booking_confirmation_template(booking=booking, email_to=email_to)
        )
        logger.info(f"Successfully send email message to '{email_to}'.")

    except (ConnectionErrors, TemplateNotFound, Exception) as e:
        msg: str = ""
        if isinstance(e, ConnectionErrors):
            msg: str = "Something problems with SMTP credentials. Details: {}".format(e)
        elif isinstance(e, TemplateNotFound):
            msg: str = "Template Not Found. Details: {}".format(e)
        elif isinstance(e, Exception):
            msg: str = "Unexpected error occurred email sending. Details: {}".format(e)

        logger.error(msg)
