from typing import List

from pydantic import BaseModel, RootModel


class RoomsSchema(BaseModel):
    """Схема для получения информации по номеру."""

    id: int
    hotel_id: int
    name: str
    description: str
    room_amenities: List
    price: int
    quantity: int
    image_id: int
    total_cost: int
    room_offers: int


class ListRoomsSchema(RootModel):
    """Схема для получения списка номеров с информацией."""

    root: List[RoomsSchema]
