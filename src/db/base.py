from typing import Any, Optional, Sequence, Tuple, Type

from loguru import logger
from sqlalchemy import Result, RowMapping, Select, insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.dml import ReturningInsert

from src.database import Base, async_session_maker, query_compile


class BaseDb:
    model: Type[Base] = None

    @classmethod
    async def find_one_or_none(cls, **filter_by) -> Optional[RowMapping]:
        async with async_session_maker() as session:
            query: Select[Tuple | Any] = select(cls.model.__table__.columns).filter_by(
                **filter_by
            )
            logger.debug(f"SQL Query: '{query_compile(query)}'")
            query_execute: Result[Tuple | Any] = await session.execute(query)
            result: Optional[RowMapping] = query_execute.mappings().one_or_none()
            logger.info(f"Result: '{result}'")
            return result

    @classmethod
    async def find_all(
        cls, limit: int = 10, page: int = 1, **filter_by
    ) -> Sequence[RowMapping]:
        async with async_session_maker() as session:
            query: Select[Tuple | Any] = (
                select(cls.model.__table__.columns)
                .filter_by(**filter_by)
                .limit(limit)
                .offset(page)
            )
            logger.debug(f"SQL Query: '{query_compile(query)}'")
            query_execute: Result[Tuple | Any] = await session.execute(query)
            result: Sequence[RowMapping] = query_execute.mappings().all()
            logger.info(f"Result: '{result}'")
            return result

    @classmethod
    async def find_like(cls, value: str):
        async with async_session_maker() as session:
            query: Select[Tuple[Any]] = select(cls.model.__table__.columns).where(
                cls.model.name.like(f"%{value}%")
            )
            logger.debug(f"SQL Query: '{query_compile(query)}'")
            query_execute: Result[Tuple | Any] = await session.execute(query)
            result: Sequence[RowMapping] = query_execute.mappings().all()
            logger.info(f"Result: '{result}'")
            return result

    @classmethod
    async def add(cls, **data) -> Optional[RowMapping] | None:
        msg: str = ""
        try:
            query: ReturningInsert[Tuple | Any] = (
                insert(cls.model).values(**data).returning(cls.model.id)
            )
            # logger.debug(f"SQL Query: '{query_compile(query)}'")
            async with async_session_maker() as session:
                query_execute: Result[Tuple | Any] = await session.execute(query)
                result: Optional[RowMapping] = query_execute.mappings().first()
                logger.info(f"Result: '{result}'")
                await session.commit()
                return result
        except (SQLAlchemyError, Exception) as e:
            if isinstance(e, SQLAlchemyError):
                msg: str = (
                    "Database Exc: Cannot insert data into table. Details: {}".format(e)
                )
            elif isinstance(e, Exception):
                msg: str = (
                    "Unknown Exc: Cannot insert data into table. Details: {}".format(e)
                )

            logger.error(msg, extra={"table": cls.model.__tablename__}, exc_info=True)
            return None
