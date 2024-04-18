import random
from datetime import date
from typing import Dict, List

from dateutil.relativedelta import relativedelta
from faker import Faker

from src.bookings.schemas import BookingSchema
from src.hotels.rooms.schemas import RoomsSchema
from src.hotels.schemas import HotelsSchema
from src.users.auth import get_password_hash
from src.users.schemas import UserSchema

faker: Faker = Faker()
amenities = ["Wi-Fi", "Бассейн", "Парковка", "Кондиционер в номере", "Тренажерный зал"]


def gen_city_data() -> List[Dict]:
    return [{"id": 1, "country_id": 1, "name": "Москва"}]


def gen_country_data() -> List[Dict]:
    return [{"id": 1, "name": "Россия"}]


def gen_hotels_data() -> List[Dict]:
    return [
        HotelsSchema.model_construct(
            name=faker.company(),
            city_id=1,
            stars=random.randint(1, 5),
            location=faker.address(),
            amenities=list(
                set(random.choices(amenities, k=random.choice(range(1, 5))))
            ),
            min_price=random.randint(5350, 12400),
            rooms_quantity=15,
        ).model_dump()
        for hotel in range(10)
    ]


def gen_rooms_data() -> List[Dict]:
    return [
        RoomsSchema.model_construct(
            name=faker.word(),
            hotel_id=room + 1,
            description=faker.text(),
            price=random.randint(5350, 12400),
            room_amenities=list(
                set(random.choices(amenities, k=random.choice(range(1, 5))))
            ),
            min_price=random.randint(5350, 12400),
            quantity=15,
        ).model_dump()
        for room in range(10)
    ]


def gen_users_data() -> List[Dict]:
    return [
        UserSchema.model_construct(
            email=faker.email(), hashed_password=get_password_hash("User123")
        ).model_dump()
        for hotel in range(10)
    ]


def gen_bookings_data() -> List[Dict]:
    return [
        BookingSchema.model_construct(
            room_id=booking + 1,
            user_id=booking + 1,
            date_from=date.today(),
            date_to=date.today() + relativedelta(days=5),
            price=random.randint(5350, 12400),
        ).model_dump()
        for booking in range(10)
    ]
