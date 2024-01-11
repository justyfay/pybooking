from typing import Type

from src.database import Base
from src.db.base import BaseDb
from src.users.models import Users


class UsersDb(BaseDb):
    model: Type[Base] = Users
