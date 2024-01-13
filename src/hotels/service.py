from datetime import date
from typing import Optional

from sqlalchemy import CTE

from src.hotels.db import HotelsDb
from src.hotels.schemas import ListHotelsWithRoomsSchema


class HotelService:
    @classmethod
    async def search_by(
        cls,
        arrival_date: date,
        departure_date: date,
        city: Optional[str] = None,
        region: Optional[str] = None,
        country: Optional[str] = None,
    ) -> ListHotelsWithRoomsSchema:
        """Метод для формирования запроса на поиск отелей по переданной локации.

        :param arrival_date: Дата заезда
        :param departure_date: Дата выезда
        :param city: Название города
        :param region: Название региона
        :param country: Название страны
        :return :class:`Sequence[RowMapping]` - список смапленных данных по отелям
        """
        booked_hotels: CTE = await HotelsDb.booked_hotels(
            arrival_date=arrival_date, departure_date=departure_date
        )
        if city is not None:
            return await HotelsDb.search_by_city(
                booked_hotels=booked_hotels, city_name=city
            )
        if region is not None:
            return await HotelsDb.search_by_region(
                booked_hotels=booked_hotels, region_name=region
            )
        if country is not None:
            return await HotelsDb.search_by_country(
                booked_hotels=booked_hotels, country_name=country
            )
