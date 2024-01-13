from typing import Dict, Optional

from fastapi import Depends, Request
from jose import ExpiredSignatureError, JWTError, jwt
from sqlalchemy import RowMapping

from config import settings
from src.exceptions import (
    IncorrectTokenFormatException,
    TokenAbsentException,
    TokenExpiredException,
    UserIsNotPresentException,
)
from src.users.db import UsersDb
from src.users.schemas import UserSchema


def get_token(request: Request) -> str:
    """Метод получения токена авторизации.

    :param request: Запрос
    :return: `str` - Токен пользователя
    """
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)) -> UserSchema:
    """Метод получения авторизованного пользователя.

    :param token: Токен пользователя
    :return :class:`UserSchema` - Авторизованный пользователь
    """
    try:
        payload: Dict = jwt.decode(token, settings.secret_key, settings.algorithm)
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user: Optional[RowMapping] = await UsersDb.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return UserSchema.model_validate(user)
