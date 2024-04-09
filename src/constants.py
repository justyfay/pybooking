from enum import Enum


class LocationsEnum(str, Enum):
    CITY = "city"
    REGION = "region"
    COUNTRY = "country"


class HotelsEnum(Enum):
    HOTELS: int = 0
    PAGES: int = 1
    COUNT_HOTELS: int = 2
