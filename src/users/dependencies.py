from fastapi import Depends, Request
from jose import jwt, ExpiredSignatureError, JWTError

from src.exceptions import TokenExpiredException, IncorrectTokenFormatException, UserIsNotPresentException, \
    TokenAbsentException
from src.users.db import UsersDb
from config import settings


def get_token(request: Request) -> str:
    token = request.cookies.get("access_token")
    if not token:
        raise TokenAbsentException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token, settings.secret_key, settings.algorithm
        )
    except ExpiredSignatureError:
        raise TokenExpiredException
    except JWTError:
        raise IncorrectTokenFormatException
    user_id: str = payload.get("sub")
    if not user_id:
        raise UserIsNotPresentException
    user = await UsersDb.find_one_or_none(id=int(user_id))
    if not user:
        raise UserIsNotPresentException

    return user
