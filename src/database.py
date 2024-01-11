from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from sqlalchemy.orm import DeclarativeBase

from config import settings


engine: AsyncEngine = create_async_engine(url=settings.database_url)
async_session_maker: async_sessionmaker[AsyncSession] = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)


class Base(DeclarativeBase):
    """Класс аккумуляции данных всех таблиц для работы с миграциями."""
    pass
