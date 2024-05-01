import math
import string
from datetime import date
from typing import List, Optional, Tuple

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Path, Query
from fastapi_cache.decorator import cache
from loguru import logger
from sqlalchemy import RowMapping
from starlette import status

from src.constants import HotelsEnum
from src.hotels.db import HotelsDb
from src.hotels.schemas import HotelsPaginate, HotelsSchema
from src.hotels.service import HotelService
from src.hotels.utils import paginate

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get(
    path="/results",
    status_code=status.HTTP_200_OK,
    response_model=HotelsPaginate,
    summary="Поиск отелей по городу, стране или региону.",
    description="Поиск отелей доступен для неавторизованных пользователей. Возвращает список отелей по указанной "
    "локации, где есть хотя бы один свободный для бронирования номер.",
    responses={
        status.HTTP_200_OK: {
            "model": HotelsPaginate,
            "description": "Ответ на успешный запрос получения списка отелей по стране.",
        }
    },
)
@cache(expire=60)
async def get_hotels(
    location_name: str = Query(default="Москва", description="Название локации"),
    location_type: str = Query(
        default="city", description="Тип локации (city, region, country)"
    ),
    arrival_date: date = Query(default=date.today(), description="Дата заезда"),
    departure_date: date = Query(
        default=date.today() + relativedelta(days=1), description="Дата выезда"
    ),
    page: int = Query(default=1, description="Страница выдачи"),
    limit: int = Query(default=10, description="Количество результатов на странице"),
    stars: str = Query(
        default=None, description="Звездность отелей в выдаче. Передаются через пробел."
    ),
) -> HotelsPaginate:
    if stars is not None:
        try:
            stars: List[int] | None = list(map(int, stars.split()))
        except ValueError:
            logger.warning(
                "Некорректное значение звезд. Параметр 'stars' принимает последовательность чисел от 0 до 5."
            )
            stars = None
    hotels = await HotelService.search_by(
        location_name=string.capwords(location_name, "-"),
        location_type=location_type,
        arrival_date=arrival_date,
        departure_date=departure_date,
        stars=stars,
    )

    hotels_with_pagination: Tuple[List, int, int] = paginate(
        items=hotels.root, limit=limit, page_number=page
    )

    hotels_info: List[HotelsSchema] = hotels_with_pagination[HotelsEnum.HOTELS.value]
    for hotel in hotels_info:
        hotel.min_price = math.ceil(hotel.min_price)

    return HotelsPaginate.model_construct(
        results=hotels_info,
        pages=hotels_with_pagination[HotelsEnum.PAGES.value],
        total=hotels_with_pagination[HotelsEnum.COUNT_HOTELS.value],
        current_page=page,
        limit=limit,
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
