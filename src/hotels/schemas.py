from __future__ import annotations

from typing import Dict, List, Optional

from pydantic import BaseModel, RootModel


class HotelsSchema(BaseModel):
    """Схема для получения информации по отелю."""

    id: int
    name: str
    city_id: int
    location: Optional[str]
    stars: int
    amenities: List[str]
    rooms_quantity: int
    min_price: Optional[float]
    coordinates: Optional[Dict]


class HotelsWithRoomsSchema(HotelsSchema):
    """Схема для получения информации по отелю с количеством свободных номеров и фотографией."""

    images: List[str] | None
    room_offers: int


class ListHotelsWithRoomsSchema(RootModel):
    """Схема получения списка отелей с информацией по номерам."""

    root: List[HotelsWithRoomsSchema]
