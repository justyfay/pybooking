from typing import Type

from src.database import Base
from src.db.base import BaseDb
from src.geo.models import City, Country, Region


class CityDb(BaseDb):
    model: Type[Base] = City


class RegionDb(BaseDb):
    model: Type[Base] = Region


class CountryDb(BaseDb):
    model: Type[Base] = Country
