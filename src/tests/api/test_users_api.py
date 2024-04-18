import pytest
from httpx import AsyncClient, Response

from src.users.schemas import UserAuthSchema


@pytest.mark.parametrize(
    "email, password, expected_status_code",
    [
        ("new_user@test.com", "fc4kjv!", 200),
        ("new_user@test.com", "fc4kjv!", 409),
        ("new_user", "fc4kjv!", 422),
    ],
)
async def test_register_user(email, password, expected_status_code, ac: AsyncClient):
    response: Response = await ac.post(
        "/auth/register",
        json=UserAuthSchema.model_construct(
            email=email, password=password
        ).model_dump(),
    )

    actual_status_code: int = response.status_code

    assert expected_status_code == actual_status_code, (
        f"Ожидаемый статус-код при регистрации пользователя '{email}' c паролем '{password}' "
        f"должен быть '{expected_status_code}'. Актуальный: '{actual_status_code}'."
    )


@pytest.mark.parametrize(
    "email, password, expected_status_code",
    [
        ("new_user@test.com", "fc4kjv!", 200),
        ("new_user@test.com", "fc4kjv", 401),
        ("new_user", "fc4kjv!", 422),
    ],
)
async def test_login_user(email, password, expected_status_code, ac: AsyncClient):
    response: Response = await ac.post(
        "/auth/login",
        json=UserAuthSchema.model_construct(
            email=email, password=password
        ).model_dump(),
    )

    actual_status_code: int = response.status_code

    assert expected_status_code == actual_status_code, (
        f"Ожидаемый статус-код при авторизации пользователя '{email}' c паролем '{password}' "
        f"должен быть '{expected_status_code}'. Актуальный: '{actual_status_code}'."
    )
