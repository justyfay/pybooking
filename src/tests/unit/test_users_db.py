from src.users.db import UsersDb


async def test_find_user_by_email(setup_test_data):
    expected_user = setup_test_data.users[0]["email"]

    user_in_db = await UsersDb.find_one_or_none(email=expected_user)
    actual_user = user_in_db["email"]

    assert (
        expected_user == actual_user
    ), f"Созданный пользователь '{expected_user}' соответствует пользователю '{actual_user}', найденному в базе."
