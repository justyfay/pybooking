import asyncio
from collections import namedtuple
from typing import Tuple, Type

import pytest
from httpx import AsyncClient
from sqlalchemy import insert

from config import settings
from src.bookings.models import Bookings
from src.database import Base, async_session_maker, engine
from src.geo.models import City, Country
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms
from src.main import app as fastapi_app
from src.tests import gen_data
from src.users.models import Users
from src.users.schemas import UserAuthSchema, UserSchema


@pytest.fixture(scope="session")
def setup_test_data() -> Type[namedtuple]:
    data: Type[Tuple] = namedtuple(
        typename="data",
        field_names=("country", "city", "hotels", "rooms", "users", "bookings"),
    )
    return data(
        country=gen_data.gen_country_data(),
        city=gen_data.gen_city_data(),
        hotels=gen_data.gen_hotels_data(),
        rooms=gen_data.gen_rooms_data(),
        users=gen_data.gen_users_data(),
        bookings=gen_data.gen_bookings_data(),
    )


@pytest.fixture(autouse=True, scope="session")
async def prepare_database(setup_test_data: Type[namedtuple]):
    assert settings.mode == "Test"

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.drop_all)
        await connection.run_sync(Base.metadata.create_all)

    async with async_session_maker() as session:
        for Model, values in [
            (Country, setup_test_data.country),
            (City, setup_test_data.city),
            (Hotels, setup_test_data.hotels),
            (Rooms, setup_test_data.rooms),
            (Users, setup_test_data.users),
            (Bookings, setup_test_data.bookings),
        ]:
            query = insert(Model).values(values)
            await session.execute(query)

        await session.commit()


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def ac():
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture(scope="session")
async def authenticated_ac(setup_test_data):
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        user: UserSchema = setup_test_data.users[0]
        await ac.post(
            "auth/login",
            json=UserAuthSchema.model_construct(
                email=user.get("email"), password="User123"
            ).model_dump(),
        )
        assert ac.cookies["access_token"]
        yield ac
