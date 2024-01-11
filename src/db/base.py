from typing import Type, Optional, Sequence, Tuple, Any

from loguru import logger
from sqlalchemy import select, insert, RowMapping, Select, Result
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.dml import ReturningInsert

from src.database import async_session_maker, Base


class BaseDb:
    model: Type[Base] = None

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Optional[RowMapping]:
        async with async_session_maker() as session:
            query: Select[Tuple | Any] = select(cls.model.__table__.columns).filter_by(**filter_by)
            result: Result[Tuple | Any] = await session.execute(query)
            return result.mappings().one_or_none()

    @classmethod
    async def find_all(cls, limit: int = 10, page: int = 1, **filter_by) -> Sequence[RowMapping]:
        async with async_session_maker() as session:
            query: Select[Tuple | Any] = select(
                cls.model.__table__.columns).filter_by(**filter_by).limit(limit).offset(page)
            result: Result[Tuple | Any] = await session.execute(query)
            return result.mappings().all()

    @classmethod
    async def add(cls, **data) -> None:
        try:
            query: ReturningInsert[Tuple | Any] = insert(cls.model).values(**data).returning(cls.model.id)
            async with async_session_maker() as session:
                result: Result[Tuple | Any] = await session.execute(query)
                await session.commit()
                return result.mappings().first()
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg: str = "Database Exc: Cannot insert data into table"
            elif isinstance(e, Exception):
                msg: str = "Unknown Exc: Cannot insert data into table"

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
