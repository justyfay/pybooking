from typing import List

from fastapi import APIRouter, Depends, Query
from starlette import status

from src.geo.schemas import (
    Feature,
    Geometry,
    Locations,
    MapSchema,
    Options,
    Properties,
)
from src.geo.service import GeoService
from src.hotels.router import get_hotels
from src.hotels.schemas import HotelsPaginate

router = APIRouter(
    prefix="/geo",
    tags=["География"],
)


@router.get(
    path="",
    status_code=status.HTTP_200_OK,
    response_model=Locations,
    summary="Поиск локаций.",
    description="Запрос вернет список локаций по совпадению в названии.",
    responses={
        status.HTTP_200_OK: {
            "model": Locations,
            "description": "Ответ на успешный запрос получения списка локаций.",
        }
    },
)
async def get_location(
    location: str = Query(
        default="Москва", description="Название города, региона или страны."
    ),
) -> Locations:
    locations = await GeoService.search_by(location=location.capitalize())
    return Locations.model_validate(locations)


@router.get(
    path="/map",
    summary="Получение объектов карты.",
    description="Получение объектов для яндекс карты.",
    responses={
        status.HTTP_200_OK: {
            "model": MapSchema,
            "description": "Ответ на успешный запрос объектов карты.",
        }
    },
)
def get_map(hotels: HotelsPaginate = Depends(get_hotels)) -> dict:
    features: List = []
    for hotel in hotels.results:
        new_feature: Feature = Feature.model_construct(
            type="Feature",
            id=hotel.id,
            geometry=Geometry.model_construct(
                type="Point",
                coordinates=[
                    hotel.coordinates.get("lat"),
                    hotel.coordinates.get("lon"),
                ],
            ),
            properties=Properties.model_construct(
                balloon_content=f"{hotel.name}\n{hotel.location}",
                cluster_caption=f"Метка с '{hotel.name}'",
                hint_content=hotel.name,
                icon_content=f"{hotel.min_price}₽",
            ),
            options=Options.model_construct(
                icon_color="#005bff", preset="islands#nightStretchyIcon"
            ),
        )
        features.append(new_feature)
    return MapSchema.model_construct(
        type="FeatureCollection", features=features
    ).model_dump(by_alias=True)
