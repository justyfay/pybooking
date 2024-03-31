from typing import List

from pydantic import BaseModel, RootModel


class GeoSchema(BaseModel):
    """Схема получения информации по локациям."""

    name: str
    type: str


class Locations(RootModel):
    root: List[GeoSchema]
