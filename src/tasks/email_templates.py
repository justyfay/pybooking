from email.message import EmailMessage

from pydantic import EmailStr

from config import settings


def create_booking_confirmation_template(
    booking: dict,
    email_to: EmailStr,
) -> EmailMessage:
    email: EmailMessage = EmailMessage()

    email["Subject"] = "Подтверждение бронирования"
    email["From"] = settings.smtp_user
    email["To"] = email_to

    email.set_content(
        f"""
                <h1>Напоминание о бронировании</h1>
                Вы забронировали отель с {booking["date_from"]} по {booking["date_to"]}
            """,
        subtype="html",
    )
    return email
