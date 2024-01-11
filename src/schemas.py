from typing import Optional

from pydantic import BaseModel

from src.exceptions import RoomFullyBooked, TokenAbsentException, UserAlreadyExistsException


class SuccessResponse(BaseModel):
    """Общая схема для успешных ответов."""
    status: str = "Success"
    detail: Optional[str] = None


class UnauthorizedResponse(BaseModel):
    """Общая схема для ответов неавторизованного пользователя."""
    detail: str = TokenAbsentException.detail


class ConflictBookingResponse(BaseModel):
    """Схема для ответов при бронировании занятых номеров."""
    detail: str = RoomFullyBooked.detail


class ConflictUsersResponse(BaseModel):
    """Схема для ответов при добавлении уже существующих пользователей."""
    detail: str = UserAlreadyExistsException.detail
