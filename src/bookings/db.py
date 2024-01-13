from datetime import date
from typing import Any, Sequence, Tuple, Type

from loguru import logger
from sqlalchemy import (
    CTE,
    Result,
    RowMapping,
    Select,
    and_,
    delete,
    func,
    insert,
    or_,
    select,
)
from sqlalchemy.sql.dml import ReturningInsert

from src.bookings.models import Bookings
from src.bookings.schemas import BookingResponseSchema, ListBookingsSchema
from src.database import Base, async_session_maker, query_compile
from src.db.base import BaseDb
from src.exceptions import RoomFullyBooked
from src.hotels.rooms.models import Rooms


class BookingDb(BaseDb):
    model: Type[Base] = Bookings

    @classmethod
    async def find_bookings_with_room_info(
        cls, user_id: int, limit: int = 10, page: int = 1
    ) -> ListBookingsSchema:
        """Метод вернет бронирования пользователя с информацией по комнатам.

        :param page: Пагинация
        :param limit: Лимит количества записей на одной странице
        :param user_id: Идентификатор пользователя, для которого ищутся бронирования
        :return :class:`ListBookingsSchema` - список бронирований
        """
        query: Select[Tuple | Any] = (
            (
                select(
                    Bookings.__table__.columns,
                    Rooms.__table__.columns,
                )
                .join(Rooms, Rooms.id == Bookings.room_id, isouter=True)
                .where(Bookings.user_id == user_id)
            )
            .limit(limit)
            .offset(page)
        )

        async with async_session_maker() as session:
            logger.debug(f"SQL Query: '{query_compile(query)}'")
            query_execute: Result[Any] = await session.execute(query)
            result: Sequence[RowMapping] = query_execute.mappings().all()
            logger.info(f"Result: '{result}'")

            return ListBookingsSchema.model_validate(result)

    @classmethod
    async def delete(cls, booking_id: int) -> None:
        """Метод для удаления записи о бронировании.

        :param booking_id: Идентификатор бронирования, которое нужно удалить
        """
        async with async_session_maker() as session:
            await session.execute(delete(Bookings).where(Bookings.id == booking_id))
            await session.commit()

    @classmethod
    async def add(
        cls, room_id: int, user_id: int, date_from: date, date_to: date
    ) -> BookingResponseSchema:
        """Метод для добавления бронирования номера по ID на указанные даты.

        :param room_id: Идентификатор комнаты, которую нужно забронировать
        :param user_id: Идентификатор пользователя
        :param date_from: Дата заезда
        :param date_to: Дата выезда
        :return :class:`BookingResponseSchema` - созданное бронирование
        """
        async with async_session_maker() as session:
            booked_rooms: CTE = (
                select(Bookings)
                .where(
                    and_(
                        Bookings.room_id == room_id,
                        or_(
                            and_(Bookings.date_from.between(date_from, date_to)),
                            and_(Bookings.date_to.between(date_from, date_to)),
                        ),
                    )
                )
                .cte("booked_rooms")
            )
            logger.debug(f"SQL Query: '{query_compile(booked_rooms)}'")
            booked_rooms_select: Select[Any] = select(booked_rooms)
            booked_rooms_execute: Result[Any] = await session.execute(
                booked_rooms_select
            )
            logger.info(f"Result: '{booked_rooms_execute.mappings().all()}'")

            all_rooms: Select[Tuple | Any] = select(Rooms.quantity).where(
                Rooms.id == room_id
            )
            all_rooms_execute: Result[Any] = await session.execute(all_rooms)
            all_rooms_result: int = all_rooms_execute.scalar()

            free_rooms: Select[Tuple | Any] = (
                select(
                    (
                        Rooms.quantity
                        - func.count(booked_rooms.c.room_id).filter(
                            booked_rooms.c.room_id.is_not(None)
                        )
                    ).label("rooms_left")
                )
                .select_from(Rooms)
                .join(booked_rooms, booked_rooms.c.room_id == Rooms.id, isouter=True)
                .where(Rooms.id == room_id)
                .group_by(Rooms.quantity, booked_rooms.c.room_id)
            )

            logger.debug(f"SQL Query: '{query_compile(free_rooms)}'")
            free_rooms_execute: Result[Any] = await session.execute(free_rooms)
            free_rooms_result: int = free_rooms_execute.scalar()
            logger.info(
                f"'{free_rooms_result}' out of '{all_rooms_result}' rooms available."
            )

            if free_rooms_result > 0:
                get_price: Select[Tuple | Any] = select(Rooms.price).filter_by(
                    id=room_id
                )
                price: Result[Tuple | Any] = await session.execute(get_price)
                price: int = price.scalar()
                add_booking: ReturningInsert = (
                    insert(Bookings)
                    .values(
                        room_id=room_id,
                        user_id=user_id,
                        date_from=date_from,
                        date_to=date_to,
                        price=price,
                    )
                    .returning(
                        Bookings.id,
                        Bookings.user_id,
                        Bookings.room_id,
                        Bookings.date_from,
                        Bookings.date_to,
                    )
                )

                new_booking_execute: Result[Any] = await session.execute(add_booking)
                new_booking_result: RowMapping = new_booking_execute.mappings().one()
                logger.info(f"Result: '{new_booking_result}'.")
                await session.commit()

                return BookingResponseSchema.model_validate(new_booking_result)
            else:
                raise RoomFullyBooked
