from typing import List, Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    city_id: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[Optional[str]]
    stars: Mapped[int]
    amenities: Mapped[List[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    images: Mapped[List[str]] = mapped_column(JSON, nullable=True)
    min_price: Mapped[Optional[float]]
    coordinates: Mapped[str] = mapped_column(JSON, nullable=True)
