from typing import Any, Optional, Tuple

from sqlalchemy import CTE, NullPool, Select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.dml import ReturningInsert

from config import settings

if settings.mode == "Test":
    database_url = settings.database_test_url
    database_params = {"poolclass": NullPool}
else:
    database_url = settings.database_url
    database_params = {}

engine: AsyncEngine = create_async_engine(url=database_url, **database_params)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)


class Base(DeclarativeBase):
    """Класс аккумуляции данных всех таблиц для работы с миграциями."""

    id: Optional[int] = None
    name: Optional[Mapped[str]] = None
    pass


def query_compile(
    query: Select[Tuple | Any] | CTE | ReturningInsert[Tuple | Any],
) -> SQLCompiler:
    """Метод вернет скомпилированный SQL-запрос. Используется для логирования.

    :param query: SQL-запрос
    :return :class:`SQLCompiler` - скомпилированный SQL-запрос.
    """
    sql_compile: SQLCompiler = query.compile(
        engine.engine, compile_kwargs={"literal_binds": True}
    )
    return sql_compile
