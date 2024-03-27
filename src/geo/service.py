from typing import Dict, List, Optional

from sqlalchemy import RowMapping

from src.geo.db import CityDb, CountryDb, RegionDb


class GeoService:
    @classmethod
    async def __get_location_names(cls, location_type: str, row_locations: RowMapping):
        locations: List[Dict[str, str]] = []
        for location in row_locations:
            locations.append(dict(type=location_type, name=location["name"]))
        return locations

    @classmethod
    async def search_by(
        cls,
        location: str,
    ) -> List:
        all_locations: List = []

        cities: Optional[RowMapping] = await CityDb.find_like(value=location)
        regions: Optional[RowMapping] = await RegionDb.find_like(value=location)
        countries: Optional[RowMapping] = await CountryDb.find_like(value=location)

        if len(cities) != 0:
            actual_cities = await cls.__get_location_names(
                location_type="city", row_locations=cities
            )
            all_locations += actual_cities
        if len(regions) != 0:
            actual_regions = await cls.__get_location_names(
                location_type="region", row_locations=regions
            )
            all_locations += actual_regions
        if len(countries) != 0:
            actual_countries = await cls.__get_location_names(
                location_type="country", row_locations=countries
            )
            all_locations += actual_countries

        return all_locations
