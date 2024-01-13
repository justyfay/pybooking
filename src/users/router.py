from typing import Optional

from fastapi import APIRouter, Response
from sqlalchemy import RowMapping
from starlette import status

from src.exceptions import UserAlreadyExistsException
from src.schemas import ConflictUsersResponse, SuccessResponse
from src.users.auth import authenticate_user, create_access_token, get_password_hash
from src.users.db import UsersDb
from src.users.schemas import UserAuthSchema, UserLoginSchema

router = APIRouter(
    prefix="/auth",
    tags=["Авторизация"],
)


@router.post(
    path="/register",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Регистрация",
    description="Регистрация нового пользователя.",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Ответ на успешный запрос регистрации пользователя.",
        },
        status.HTTP_409_CONFLICT: {
            "model": ConflictUsersResponse,
            "description": "Ответ на запрос при попытке зарегистрировать существующего пользователя.",
        },
    },
)
async def user_register(user_data: UserAuthSchema) -> None:
    user_exist: Optional[RowMapping] = await UsersDb.find_one_or_none(
        email=user_data.email
    )
    if user_exist:
        raise UserAlreadyExistsException
    hashed_password: str = get_password_hash(user_data.password)
    await UsersDb.add(email=user_data.email, hashed_password=hashed_password)


@router.post(
    path="/login",
    response_model=UserLoginSchema,
    status_code=status.HTTP_200_OK,
    summary="Авторизация",
    description="Авторизация существующего пользователя.",
    responses={
        status.HTTP_200_OK: {
            "model": UserLoginSchema,
            "description": "Ответ на успешный запрос авторизации пользователя.",
        }
    },
)
async def user_login(response: Response, user_data: UserAuthSchema) -> UserLoginSchema:
    user: Optional[RowMapping] = await authenticate_user(
        user_data.email, user_data.password
    )
    access_token: str = create_access_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True, expires=3600)
    return UserLoginSchema.model_construct(access_token=access_token)


@router.post(
    path="/logout",
    response_model=SuccessResponse,
    status_code=status.HTTP_200_OK,
    summary="Выход",
    description="Logout авторизованного пользователя из системы.",
    responses={
        status.HTTP_200_OK: {
            "model": SuccessResponse,
            "description": "Ответ на успешный запрос выхода пользователя.",
        }
    },
)
async def user_logout(response: Response) -> None:
    response.delete_cookie("access_token")
