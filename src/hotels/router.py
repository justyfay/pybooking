from datetime import date
from typing import Optional

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Path, Query
from sqlalchemy import RowMapping
from starlette import status

from src.hotels.db import HotelsDb
from src.hotels.schemas import HotelsSchema, ListHotelsWithRoomsSchema
from src.hotels.service import HotelService

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get(
    path="/city/results",
    status_code=status.HTTP_200_OK,
    response_model=ListHotelsWithRoomsSchema,
    summary="Поиск отелей по городу",
    description="Поиск отелей доступен для неавторизованных пользователей. Возвращает список отелей по городу, "
    "где есть хотя бы один свободный для бронирования номер.",
    responses={
        status.HTTP_200_OK: {
            "model": ListHotelsWithRoomsSchema,
            "description": "Ответ на успешный запрос получения списка отелей по городу.",
        }
    },
)
async def get_hotels_by_city(
    city_name: str = Query(
        default="Сыктывкар", description="Название города. Не чувствителен к регистру."
    ),
    arrival_date: date = Query(default=date.today(), description="Дата заезда"),
    departure_date: date = Query(
        default=date.today() + relativedelta(days=1), description="Дата выезда"
    ),
) -> ListHotelsWithRoomsSchema:
    return await HotelService.search_by(
        city=city_name.capitalize(),
        arrival_date=arrival_date,
        departure_date=departure_date,
    )


@router.get(
    path="/region/results",
    status_code=status.HTTP_200_OK,
    response_model=ListHotelsWithRoomsSchema,
    summary="Поиск отелей по региону",
    description="Поиск отелей доступен для неавторизованных пользователей. Возвращает список отелей по региону, "
    "где есть хотя бы один свободный для бронирования номер.",
    responses={
        status.HTTP_200_OK: {
            "model": ListHotelsWithRoomsSchema,
            "description": "Ответ на успешный запрос получения списка отелей по региону.",
        }
    },
)
async def get_hotels_by_region(
    region_name: str = Query(
        default="Алтай", description="Название региона. Не чувствителен к регистру."
    ),
    arrival_date: date = Query(default=date.today(), description="Дата заезда"),
    departure_date: date = Query(
        default=date.today() + relativedelta(days=1), description="Дата выезда"
    ),
) -> ListHotelsWithRoomsSchema:
    return await HotelService.search_by(
        region=region_name.capitalize(),
        arrival_date=arrival_date,
        departure_date=departure_date,
    )


@router.get(
    path="/country/results",
    status_code=status.HTTP_200_OK,
    response_model=ListHotelsWithRoomsSchema,
    summary="Поиск отелей по стране",
    description="Поиск отелей доступен для неавторизованных пользователей. Возвращает список отелей по стране, "
    "где есть хотя бы один свободный для бронирования номер.",
    responses={
        status.HTTP_200_OK: {
            "model": ListHotelsWithRoomsSchema,
            "description": "Ответ на успешный запрос получения списка отелей по стране.",
        }
    },
)
async def get_hotels_by_country(
    country_name: str = Query(
        default="Россия", description="Название страны. Не чувствителен к регистру."
    ),
    arrival_date: date = Query(default=date.today(), description="Дата заезда"),
    departure_date: date = Query(
        default=date.today() + relativedelta(days=1), description="Дата выезда"
    ),
) -> ListHotelsWithRoomsSchema:
    return await HotelService.search_by(
        country=country_name.capitalize(),
        arrival_date=arrival_date,
        departure_date=departure_date,
    )


@router.get(
    path="/{hotel_id}",
    status_code=status.HTTP_200_OK,
    response_model=HotelsSchema,
    summary="Получение отеля",
    description="Получение отеля по ID. Возможно получить отеля даже без свободных номеров.",
    responses={
        status.HTTP_200_OK: {
            "model": HotelsSchema,
            "description": "Ответ на успешный запрос получения отеля.",
        }
    },
)
async def get_hotel_by_id(
    hotel_id: int = Path(description="Идентификатор отеля"),
) -> HotelsSchema:
    hotel: Optional[RowMapping] = await HotelsDb.find_one_or_none(id=hotel_id)
    return HotelsSchema.model_validate(hotel)
