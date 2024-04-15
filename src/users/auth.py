from datetime import UTC, date, datetime, timedelta
from typing import Optional

from jose import jwt
from passlib.context import CryptContext
from pydantic import EmailStr
from sqlalchemy import RowMapping

from config import settings
from src.users.db import UsersDb

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode: dict = data.copy()
    expire: date = datetime.now(UTC).replace(tzinfo=None) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt: str = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str) -> bool | RowMapping:
    user: Optional[RowMapping] = await UsersDb.find_one_or_none(email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user
