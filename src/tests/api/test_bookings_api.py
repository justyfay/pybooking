from datetime import date

from dateutil.relativedelta import relativedelta
from httpx import AsyncClient

from src.bookings.schemas import BookingResponseSchema, NewBookingSchema


async def test_add_booking(authenticated_ac: AsyncClient):
    add_booking_response = await authenticated_ac.post(
        "/bookings",
        json=NewBookingSchema.model_construct(
            room_id=1,
            user_id=1,
            date_from=date.today().strftime("%Y-%m-%d"),
            date_to=(date.today() + relativedelta(days=5)).strftime("%Y-%m-%d"),
        ).model_dump(),
    )

    assert (
        add_booking_response.status_code == 200
    ), "Статус-код ответа на добавление бронирования должен быть 200"
    expected_booking = BookingResponseSchema.model_validate(
        add_booking_response.json()
    ).id

    get_bookings_response = await authenticated_ac.get("/bookings")
    actual_booking = BookingResponseSchema.model_validate(
        get_bookings_response.json()[0]
    ).id
    assert expected_booking == actual_booking, (
        f"ID '{expected_booking}' добавленного бронирования должно соответствовать ID бронирования '{actual_booking}' "
        f"в списке пользователя"
    )
