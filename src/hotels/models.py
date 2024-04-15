from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.hotels.rooms.models import Rooms


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

    rooms: Mapped[list["Rooms"]] = relationship(back_populates="hotel")

    def __str__(self):
        return f"Отель {self.name} {self.location[:30]}"
