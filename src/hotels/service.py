from datetime import date
from typing import List, Optional

from sqlalchemy import CTE

from src.constants import LocationsEnum
from src.hotels.db import HotelsDb
from src.hotels.schemas import ListHotelsWithRoomsSchema


class HotelService:
    @classmethod
    async def search_by(
        cls,
        arrival_date: date,
        departure_date: date,
        location_type: str,
        location_name: str,
        stars: Optional[List[int]],
    ) -> ListHotelsWithRoomsSchema:
        """Метод для формирования запроса на поиск отелей по переданной локации.

        :param arrival_date: Дата заезда
        :param departure_date: Дата выезда
        :param location_type: Тип локации
        :param location_name: Название локации
        :param stars: Звездность отеля
        :return :class: `ListHotelsWithRoomsSchema` - список отелей
        """
        booked_hotels: CTE = await HotelsDb.booked_hotels(
            arrival_date=arrival_date, departure_date=departure_date
        )
        match location_type:
            case LocationsEnum.CITY.value:
                return await HotelsDb.search_by_city(
                    booked_hotels=booked_hotels, city_name=location_name, stars=stars
                )
            case LocationsEnum.REGION.value:
                return await HotelsDb.search_by_region(
                    booked_hotels=booked_hotels, region_name=location_name, stars=stars
                )
            case LocationsEnum.COUNTRY.value:
                return await HotelsDb.search_by_country(
                    booked_hotels=booked_hotels, country_name=location_name, stars=stars
                )
