from typing import List

from pydantic import BaseModel


class RoomsSchema(BaseModel):
    """Схема для получения информации по номерам."""
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
