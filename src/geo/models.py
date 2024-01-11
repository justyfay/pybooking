from datetime import datetime, UTC

from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import mapped_column, Mapped

from src.database import Base


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.now(UTC).replace(tzinfo=None))


class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    name: Mapped[str]
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.now(UTC).replace(tzinfo=None))


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    name: Mapped[str]
    created_at: Mapped[str] = mapped_column(TIMESTAMP, default=datetime.now(UTC).replace(tzinfo=None))
