from datetime import date
from typing import Any, List, Optional, Sequence, Tuple, Type

from loguru import logger
from sqlalchemy import CTE, Result, RowMapping, Select, and_, func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.bookings.models import Bookings
from src.database import Base, async_session_maker, query_compile
from src.db.base import BaseDb
from src.geo.models import City, Country, Region
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms
from src.hotels.schemas import ListHotelsWithRoomsSchema


class HotelsDb(BaseDb):
    model: Type[Base] = Hotels

    @classmethod
    async def filter_hotels(
        cls,
        session: AsyncSession,
        hotels_with_free_rooms: Select[Tuple[Any, Any]],
        stars: Optional[List[int]],
    ) -> Result[Any]:
        """Метод отфильтрует отели при запросе в БД, если фильтры по звездам были переданы.

        :param session: Объект сессии для взаимодействия с БД
        :param hotels_with_free_rooms: Запрос на получение отелей со свободными комнатами
        :param stars: Звезды отеля для фильтрации
        :return :class:`Result` - результат запроса на отели
        """
        if stars is None:
            hotels_execute: Result[Any] = await session.execute(hotels_with_free_rooms)
        else:
            stars_for_db: List = []
            for star in stars:
                stars_for_db.append(Hotels.stars == star)
            hotels_execute: Result[Any] = await session.execute(
                hotels_with_free_rooms.filter(or_(*stars_for_db))
            )
        return hotels_execute

    @classmethod
    async def booked_hotels(cls, arrival_date: date, departure_date: date) -> CTE:
        """Метод вернет отели по искомому городу, где есть хотя бы один свободный номер.

        :param arrival_date: Дата заезда
        :param departure_date: Дата выезда
        :return :class:`CTE` - Подзапрос на получение отелей со свободными номерами
        """
        booked_rooms: CTE = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .select_from(Bookings)
            .where(
                or_(
                    and_(Bookings.date_from.between(arrival_date, departure_date)),
                    and_(Bookings.date_to.between(arrival_date, departure_date)),
                ),
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )

        booked_hotels: CTE = (
            select(
                Rooms.hotel_id,
                func.sum(
                    Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)
                ).label("room_offers"),
            )
            .select_from(Rooms)
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .group_by(Rooms.hotel_id)
            .cte("booked_hotels")
        )
        return booked_hotels

    @classmethod
    async def search_by_city(
        cls,
        booked_hotels: CTE,
        city_name: str,
        stars: Optional[List[int]],
    ) -> ListHotelsWithRoomsSchema:
        """Метод вернет отели по искомому городу, где есть хотя бы один свободный номер.

        :param booked_hotels: Подзапрос на получение отелей со свободными номерами
        :param city_name: Название города, по которому происходит поиск
        :param stars: Звезды для фильтрации отелей
        :return :class:`ListHotelsWithRoomsSchema` - список данных по отелям
        """
        hotels_with_free_rooms_in_city: Select[Tuple[Any, Any]] = (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.room_offers,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .join(City, Hotels.city_id == City.id)
            .where(City.name.like(f"%{city_name}%"))
        )

        async with async_session_maker() as session:
            logger.debug(
                f"SQL Query: '{query_compile(hotels_with_free_rooms_in_city)}'"
            )
            hotels_execute: Result[Any] = await cls.filter_hotels(
                session=session,
                hotels_with_free_rooms=hotels_with_free_rooms_in_city,
                stars=stars,
            )
            hotels_result: Sequence[RowMapping] = hotels_execute.mappings().all()
            logger.info(f"Result: '{hotels_result}'")

        return ListHotelsWithRoomsSchema.model_validate(hotels_result)

    @classmethod
    async def search_by_region(
        cls, booked_hotels: CTE, region_name: str, stars: Optional[List[int]]
    ) -> ListHotelsWithRoomsSchema:
        """Метод вернет отели по искомому региону, где есть хотя бы один свободный номер.

        :param booked_hotels: Подзапрос на получение отелей со свободными номерами
        :param region_name: Название региона, по которому происходит поиск
        :param stars: Звезды для фильтрации отелей
        :return :class:`ListHotelsWithRoomsSchema` - список данных по отелям
        """
        hotels_with_free_rooms_in_region: Select[Tuple[Any, Any]] = (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.room_offers,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .join(City, Hotels.city_id == City.id)
            .join(Region, City.region_id == Region.id)
            .where(Region.name.like(f"%{region_name}%"))
        )

        async with async_session_maker() as session:
            logger.debug(
                f"SQL Query: '{query_compile(hotels_with_free_rooms_in_region)}'"
            )
            hotels_execute: Result[Any] = await cls.filter_hotels(
                session=session,
                hotels_with_free_rooms=hotels_with_free_rooms_in_region,
                stars=stars,
            )
            hotels_result: Sequence[RowMapping] = hotels_execute.mappings().all()
            logger.info(f"Result: '{hotels_result}'")

            return ListHotelsWithRoomsSchema.model_validate(hotels_result)

    @classmethod
    async def search_by_country(
        cls, booked_hotels: CTE, country_name: str, stars: Optional[List[int]]
    ) -> ListHotelsWithRoomsSchema:
        """Метод вернет отели по искомой стране, где есть хотя бы один свободный номер.

        :param booked_hotels: Подзапрос на получение отелей со свободными номерами
        :param country_name: Название страны, по которому происходит поиск
        :param stars: Звезды для фильтрации отелей
        :return :class:`ListHotelsWithRoomsSchema` - список данных по отелям
        """
        hotels_with_free_rooms_in_country: Select[Tuple[Any, Any]] = (
            select(
                Hotels.__table__.columns,
                booked_hotels.c.room_offers,
            )
            .join(booked_hotels, booked_hotels.c.hotel_id == Hotels.id, isouter=True)
            .join(City, Hotels.city_id == City.id)
            .join(Region, City.region_id == Region.id)
            .join(Country, Region.country_id == Country.id)
            .where(Country.name.like(f"%{country_name}%"))
        )

        async with async_session_maker() as session:
            logger.debug(
                f"SQL Query: '{query_compile(hotels_with_free_rooms_in_country)}'"
            )
            hotels_execute: Result[Any] = await cls.filter_hotels(
                session=session,
                hotels_with_free_rooms=hotels_with_free_rooms_in_country,
                stars=stars,
            )
            hotels_result: Sequence[RowMapping] = hotels_execute.mappings().all()
            logger.info(f"Result: '{hotels_result}'")

            return ListHotelsWithRoomsSchema.model_validate(hotels_result)
