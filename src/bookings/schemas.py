from datetime import date
from typing import List

from dateutil.relativedelta import relativedelta
from pydantic import BaseModel, Field


class BookingSchema(BaseModel):
    """Схема для получения информации по бронированиям."""
    id: int
    room_id: int
    user_id: int
    date_from: date
    date_to: date
    price: int
    total_cost: int
    total_days: int
    name: str
    image_id: int
    description: str
    room_amenities: List

    class Config:
        from_attributes = True


class NewBookingSchema(BaseModel):
    """Схема для добавления новых бронирований."""
    room_id: int
    user_id: int
    date_from: date
    date_to: date = Field(default=date.today() + relativedelta(days=1))

    class Config:
        from_attributes = True


class BookingResponseSchema(BaseModel):
    """Схема ответа на добавление нового бронирования."""
    id: int
    user_id: int
    room_id: int
    date_from: date
    date_to: date

    class Config:
        from_attributes = True
