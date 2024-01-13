from datetime import UTC, datetime

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Country(Base):
    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=datetime.now(UTC).replace(tzinfo=None)
    )


class Region(Base):
    __tablename__ = "region"

    id: Mapped[int] = mapped_column(primary_key=True)
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    name: Mapped[str]
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=datetime.now(UTC).replace(tzinfo=None)
    )


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    region_id: Mapped[int] = mapped_column(ForeignKey("region.id"))
    name: Mapped[str]
    created_at: Mapped[str] = mapped_column(
        TIMESTAMP, default=datetime.now(UTC).replace(tzinfo=None)
    )
