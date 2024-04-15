from fastapi import HTTPException
from starlette import status


class BookingException(HTTPException):
    status_code: int = 500
    detail: str = None

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.detail)


class UserAlreadyExistsException(BookingException):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "Пользователь уже существует"


class TokenExpiredException(BookingException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Срок действия токена истек"


class TokenAbsentException(BookingException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Отсутствует токен авторизации"


class IncorrectTokenFormatException(BookingException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Неверный формат токена"


class UserIsNotPresentException(BookingException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Пользователь не существует"


class UserNotCorrectCredentialsException(BookingException):
    status_code: int = status.HTTP_401_UNAUTHORIZED
    detail: str = "Неверный логин или пароль"


class RoomFullyBooked(BookingException):
    status_code: int = status.HTTP_409_CONFLICT
    detail: str = "Не осталось свободных номеров"
