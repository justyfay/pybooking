from datetime import date

import pytest
from dateutil.relativedelta import relativedelta

from src.bookings.db import BookingDb


@pytest.mark.parametrize(
    "expected_user_id, expected_room_id",
    [
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
    ],
)
async def test_add_booking(expected_user_id, expected_room_id):
    new_booking = await BookingDb.add(
        user_id=expected_user_id,
        room_id=expected_room_id,
        date_from=date.today(),
        date_to=date.today() + relativedelta(days=5),
    )

    assert new_booking.user_id == expected_user_id, (
        f"Ожидаемый ID пользователя '{expected_user_id}' при добавлении бронирования "
        f"соответствует актуальному '{new_booking.user_id}'."
    )
    assert new_booking.room_id == expected_room_id, (
        f"Ожидаемый ID номера '{expected_room_id}' при добавлении бронирования "
        f"соответствует актуальному '{new_booking.room_id}'."
    )

    new_booking = await BookingDb.find_one_or_none(id=new_booking.id)

    assert new_booking is not None, f"Бронирование '{new_booking.id}' добавлено в БД."


async def test_booking_delete(setup_test_data):
    booking_id = setup_test_data.bookings[-1].get("id")

    await BookingDb.delete(booking_id=booking_id)
    deleted_booking = await BookingDb.find_one_or_none(id=booking_id)
    assert deleted_booking is None, f"Бронирование '{booking_id}' удалено из БД."
