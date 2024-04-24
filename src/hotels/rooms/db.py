from datetime import date
from typing import Any, Sequence, Tuple, Type

from sqlalchemy import CTE, Result, RowMapping, Select, and_, func, or_, select

from src.bookings.models import Bookings
from src.database import Base, async_session_maker, query_compile
from src.db.base import BaseDb
from src.hotels.rooms.models import Rooms
from src.hotels.rooms.schemas import ListRoomsSchema
from src.logger import logger


class RoomsDb(BaseDb):
    model: Type[Base] = Rooms

    @classmethod
    async def find_rooms(
        cls, hotel_id: int, arrival_date: date, departure_date: date
    ) -> ListRoomsSchema:
        """Метод вернет номера с информацией по указанному отелю.

        :param hotel_id: Идентификатор отеля, по которому нужно получить комнаты
        :param arrival_date: Дата заезда
        :param departure_date: Дата выезда
        :return :class:`ListRoomsSchema` - список данных по комнатам
        """
        booked_rooms: CTE = (
            select(Bookings.room_id, func.count(Bookings.room_id).label("rooms_booked"))
            .where(
                or_(
                    and_(Bookings.date_from.between(arrival_date, departure_date)),
                    and_(Bookings.date_to.between(arrival_date, departure_date)),
                )
            )
            .group_by(Bookings.room_id)
            .cte("booked_rooms")
        )
        room_offers: Select[Tuple[Any]] = (
            select(
                Rooms.__table__.columns,
                (Rooms.price * (departure_date - arrival_date).days).label(
                    "total_cost"
                ),
                (Rooms.quantity - func.coalesce(booked_rooms.c.rooms_booked, 0)).label(
                    "room_offers"
                ),
            )
            .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
            .where(Rooms.hotel_id == hotel_id)
        )

        async with async_session_maker() as session:
            logger.debug(f"SQL Query: '{query_compile(room_offers)}'")
            rooms_execute: Result[Any] = await session.execute(room_offers)
            rooms_result: Sequence[RowMapping] = rooms_execute.mappings().all()
            logger.info(f"Result: '{rooms_result}'")

            return ListRoomsSchema.model_validate(rooms_result)
