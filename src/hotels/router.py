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
    path="/results",
    status_code=status.HTTP_200_OK,
    response_model=ListHotelsWithRoomsSchema,
    summary="Поиск отелей по городу, стране или региону.",
    description="Поиск отелей доступен для неавторизованных пользователей. Возвращает список отелей по стране, "
    "где есть хотя бы один свободный для бронирования номер.",
    responses={
        status.HTTP_200_OK: {
            "model": ListHotelsWithRoomsSchema,
            "description": "Ответ на успешный запрос получения списка отелей по стране.",
        }
    },
)
async def get_hotels(
    location_name: str = Query(default="Москва", description="Название локации"),
    location_type: str = Query(
        default="city", description="Тип локации (city, region, country)"
    ),
    arrival_date: date = Query(default=date.today(), description="Дата заезда"),
    departure_date: date = Query(
        default=date.today() + relativedelta(days=1), description="Дата выезда"
    ),
) -> ListHotelsWithRoomsSchema:
    return await HotelService.search_by(
        location_name=location_name.capitalize(),
        location_type=location_type,
        arrival_date=arrival_date,
        departure_date=departure_date,
    )


@router.get(
    path="/{hotel_id}",
    status_code=status.HTTP_200_OK,
    response_model=HotelsSchema,
    summary="Получение отеля",
    description="Получение отеля по ID. Возможно получить отели без свободных номеров.",
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
