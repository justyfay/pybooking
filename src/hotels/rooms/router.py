from datetime import date

from dateutil.relativedelta import relativedelta
from fastapi import APIRouter, Path, Query
from starlette import status

from src.hotels.rooms.db import RoomsDb
from src.hotels.rooms.schemas import ListRoomsSchema

router = APIRouter(
    prefix="/hotels",
    tags=["Отели"],
)


@router.get(
    path="/{hotel_id}/offers",
    status_code=status.HTTP_200_OK,
    response_model=ListRoomsSchema,
    summary="Получение комнат в отеле",
    description="Получение комнат в выбранном отеле.",
    responses={
        status.HTTP_200_OK: {
            "model": ListRoomsSchema,
            "description": "Ответ на успешный запрос получения списка комнат.",
        }
    },
)
async def get_rooms(
    hotel_id: int = Path(description="Идентификатор отеля"),
    arrival_date: date = Query(default=date.today(), description="Дата заезда"),
    departure_date: date = Query(
        default=date.today() + relativedelta(days=1), description="Дата выезда"
    ),
) -> ListRoomsSchema:
    room_offers = await RoomsDb.find_rooms(
        hotel_id=hotel_id, arrival_date=arrival_date, departure_date=departure_date
    )
    return room_offers
