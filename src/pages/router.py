from datetime import date

from fastapi import APIRouter, Depends, Query, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette import status

from src.hotels.router import get_hotels

templates = Jinja2Templates(directory="src/templates")

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
    hotels=Depends(get_hotels),
):
    return templates.TemplateResponse(
        "search.html",
        {
            "request": request,
            "location_name": location_name,
            "hotels": hotels.root,
            "location_type": location_type,
            "arrival_date": arrival_date,
            "departure_date": departure_date,
        },
    )
