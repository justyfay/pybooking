from datetime import date
from typing import Optional, Sequence

from sqlalchemy import CTE, RowMapping

from src.hotels.db import HotelsDb


class HotelService:

    @classmethod
    async def search_by(
            cls,
            arrival_date: date,
            departure_date: date,
            city: Optional[str] = None,
            region: Optional[str] = None,
            country: Optional[str] = None,
    ) -> Sequence[RowMapping]:
        booked_hotels: CTE = await HotelsDb.booked_hotels(arrival_date=arrival_date, departure_date=departure_date)
        if city is not None:
            return await HotelsDb.search_by_city(booked_hotels=booked_hotels, city_name=city)
        if region is not None:
            return await HotelsDb.search_by_region(booked_hotels=booked_hotels, region_name=region)
        if country is not None:
            return await HotelsDb.search_by_country(booked_hotels=booked_hotels, country_name=country)


