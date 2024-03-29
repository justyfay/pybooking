from typing import List

from fastapi import APIRouter, Query
from starlette import status

from src.geo.schemas import GeoSchema
from src.geo.service import GeoService

router = APIRouter(
    prefix="/geo",
    tags=["География"],
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=List[GeoSchema],
    summary="Поиск локаций.",
    description="Запрос вернет список локаций по совпадению в названии.",
    responses={
        status.HTTP_200_OK: {
            "model": List[GeoSchema],
            "description": "Ответ на успешный запрос получения списка локаций.",
        }
    },
)
async def get_location(
    location: str = Query(
        default="Москва", description="Название города, региона или страны."
    ),
) -> List[GeoSchema]:
    return await GeoService.search_by(location=location.capitalize())
