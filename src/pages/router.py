from datetime import date

import boto3
from botocore.exceptions import BotoCoreError
from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from loguru import logger
from starlette import status

import config
from src.hotels.router import get_hotels
from src.hotels.schemas import HotelsPaginate


def get_hotel_img(hotel_id: int) -> str:
    s3 = boto3.client(
        service_name="s3",
        region_name="ru-1",
        aws_access_key_id=config.settings.s3_access_key,
        aws_secret_access_key=config.settings.s3_secret_key,
        endpoint_url=config.settings.s3_url,
    )
    try:
        url = s3.generate_presigned_url(
            "get_object",
            Params={"Bucket": "public-bucket", "Key": f"hotel_{hotel_id}.jpg"},
            ExpiresIn=3600,
        )
        return url
    except BotoCoreError as e:
        logger.error(e)


templates = Jinja2Templates(directory="src/templates")
templates.env.globals.update(get_hotel_img=get_hotel_img)

router = APIRouter(
    prefix="",
    tags=["Страницы"],
)


@router.get(
    path="/",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    summary="Главная страница.",
)
async def get_main_page(request: Request):
    return templates.TemplateResponse("main.html", {"request": request})


@router.get(
    path="/search",
    response_class=HTMLResponse,
    status_code=status.HTTP_200_OK,
    summary="Страница с результатами поиска.",
)
async def get_search_page(
    request: Request,
    location_name: str = Query(default="Москва", description="Название локации."),
    location_type: str = Query(default="city", description="Тип локации."),
    arrival_date: date = Query(default=date.today(), description="Дата заезда."),
    departure_date: date = Query(default=date.today(), description="Дата выезда."),
    hotels: HotelsPaginate = Depends(get_hotels),
):
    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "location_name": location_name,
            "hotels": hotels.results,
            "location_type": location_type,
            "arrival_date": arrival_date,
            "departure_date": departure_date,
            "current_page": hotels.current_page,
            "pages": hotels.pages,
            "limit": hotels.limit,
        },
    )
