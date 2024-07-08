from typing import List

from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Environment, PackageLoader, select_autoescape
from pydantic import EmailStr

from config import settings

env: Environment = Environment(
    loader=PackageLoader("src", "templates/mail_templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class Mail:
    def __init__(self, url: str, email: List[EmailStr]):
        self.sender = f"{settings.smtp_sender} <{settings.smtp_user}>"
        self.email = email
        self.url = url

    async def send_mail(
        self,
        subject: str,
        message_text: str,
        button_name: str,
        small_notice: str,
        template: str,
    ):
        template = env.get_template(f"{template}.html")

        html = template.render(
            url=self.url,
            subject=subject,
            message_text=message_text,
            button_name=button_name,
            small_notice=small_notice,
        )

        message = MessageSchema(
            subject=subject,
            recipients=self.email,
            template_body=html,
            subtype=MessageType.html,
        )
        mail_conf = ConnectionConfig(
            MAIL_USERNAME=settings.smtp_user,
            MAIL_PASSWORD=settings.smtp_password,
            MAIL_FROM=settings.smtp_user,
            MAIL_PORT=settings.smtp_port,
            MAIL_SERVER=settings.smtp_host,
            MAIL_FROM_NAME=settings.smtp_sender,
            MAIL_STARTTLS=True,
            MAIL_SSL_TLS=False,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
            TEMPLATE_FOLDER="src/templates/mail_templates",
        )

        await FastMail(mail_conf).send_message(message)

    async def create_booking_confirmation_template(
        self,
        booking: dict,
        email_to: EmailStr,
    ):
        await self.send_mail(
            subject="Подтверждение бронирования",
            message_text=f"Вы забронировали отель '{booking['hotel']['name']}'. "
            f"с {booking['date_from']} по {booking['date_to']}.\n"
            f"Итоговая стоимость: {booking['booking_info']['total_cost']}.\n"
            f"Удобства и услуги в отеле: {booking['hotel']['amenities'][0]}.\n"
            f"Адрес: {booking['hotel']['location']}.",
            button_name="Проверить бронирования",
            small_notice=f"Данное письмо было сформировано для адреса {email_to}",
            template="booking_confirmation",
        )
