from typing import List, Sequence

from fastapi import APIRouter, Depends, Query, Path
from sqlalchemy import RowMapping
from starlette import status

from src.bookings.db import BookingDb
from src.bookings.schemas import BookingSchema, NewBookingSchema, BookingResponseSchema
from src.schemas import UnauthorizedResponse, ConflictBookingResponse
from src.users.dependencies import get_current_user
from src.users.models import Users

router = APIRouter(
    prefix="/bookings",
    tags=["Бронирования"],
    responses={
        status.HTTP_401_UNAUTHORIZED: {
            "model": UnauthorizedResponse,
            "description": "Ответ на запрос от неавторизованного пользователя.",
        },
    }
)


@router.get(
    path="",
    response_model=List[BookingSchema],
    status_code=status.HTTP_200_OK,
    summary="Список бронирований",
    description="Получение списка бронирований авторизованного пользователя.",
    responses={
        status.HTTP_200_OK: {
            "model": List[BookingSchema],
            "description": "Ответ на успешный запрос получения списка бронирований.",
        },
    }
)
async def get_bookings(
        user: Users = Depends(get_current_user),
        limit: int = Query(10, description="Количество бронирований на одной странице"),
        page: int = Query(1, description="Пагинация"),
) -> Sequence[RowMapping]:
    return await BookingDb.find_bookings_with_room_info(user_id=user.id, limit=limit, page=page)


@router.post(
    path="",
    response_model=BookingResponseSchema,
    status_code=status.HTTP_200_OK,
    summary="Добавление нового бронирования",
    description="Добавление бронирований доступно только для авторизованных пользователей.",
    responses={
        status.HTTP_200_OK: {
            "model": BookingResponseSchema,
            "description": "Ответ на успешный запрос добавления бронирования.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ConflictBookingResponse,
            "description": "Ответ на запрос при попытке забронировать занятый номер.",
        },
    }
)
async def add_booking(
        booking_data: NewBookingSchema,
        user: Users = Depends(get_current_user),
) -> RowMapping:
    return await BookingDb.add(
        room_id=booking_data.room_id,
        user_id=user.id,
        date_from=booking_data.date_from,
        date_to=booking_data.date_to
    )


@router.delete(
    path="/{booking_id}/cancel",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Отмена бронирования",
    description="Отмена существующего бронирования.",
)
async def delete_booking(
        booking_id: int = Path(..., description="ID бронирования для удаления."),
):
    return await BookingDb.delete(booking_id)
