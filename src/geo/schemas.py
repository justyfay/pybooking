from pydantic import BaseModel


class GeoSchema(BaseModel):
    """Схема получения информации по локациям."""

    name: str
    type: str
