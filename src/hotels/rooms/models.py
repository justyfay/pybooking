from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base

if TYPE_CHECKING:
    from src.bookings.models import Bookings
    from src.hotels.models import Hotels


class Rooms(Base):
    __tablename__ = "rooms"

    id: Mapped[int] = mapped_column(primary_key=True)
    hotel_id: Mapped[int] = mapped_column(ForeignKey("hotels.id"))
    name: Mapped[str]
    description: Mapped[Optional[str]]
    price: Mapped[int]
    room_amenities: Mapped[list[str]] = mapped_column(JSON)
    quantity: Mapped[int]
    images: Mapped[List[str]] = mapped_column(JSON, nullable=True)

    hotel: Mapped["Hotels"] = relationship(back_populates="rooms")
    bookings: Mapped[list["Bookings"]] = relationship(back_populates="room")

    def __str__(self):
        return f"Номер {self.name}"
