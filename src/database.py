from typing import Any, Optional, Tuple

from sqlalchemy import CTE, Select
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.sql.compiler import SQLCompiler
from sqlalchemy.sql.dml import ReturningInsert

from config import settings

engine: AsyncEngine = create_async_engine(url=settings.database_url)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine, expire_on_commit=False
)


class Base(DeclarativeBase):
    """Класс аккумуляции данных всех таблиц для работы с миграциями."""

    id: Optional[int] = None
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
