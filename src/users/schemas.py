from pydantic import BaseModel, EmailStr


class UserSchema(BaseModel):
    """Схема чтения пользователя."""

    id: int
    email: EmailStr
    hashed_password: str


class UserAuthSchema(BaseModel):
    """Схема для отправки данных на авторизацию."""

    email: EmailStr
    password: str


class UserLoginSchema(BaseModel):
    """Схема ответа успешной авторизации."""

    access_token: str
