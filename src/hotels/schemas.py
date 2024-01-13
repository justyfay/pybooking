from __future__ import annotations

from typing import List

from pydantic import BaseModel, RootModel


class HotelsSchema(BaseModel):
    """Схема для получения информации по отелю."""

    id: int
    name: str
    city_id: int
    location: str
    stars: int
    amenities: List
    rooms_quantity: int


class HotelsWithRoomsSchema(HotelsSchema):
    """Схема для получения информации по отелю с количеством свободных номеров и фотографией."""

    image_id: int
    room_offers: int


class ListHotelsWithRoomsSchema(RootModel):
    """Схема получения списка отелей с информацией по номерам."""

    root: List[HotelsWithRoomsSchema]
