from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Hotels(Base):
    __tablename__ = "hotels"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    city_id: Mapped[int] = mapped_column(nullable=False)
    location: Mapped[str]
    stars: Mapped[int]
    amenities: Mapped[list[str]] = mapped_column(JSON)
    rooms_quantity: Mapped[int]
    image_id: Mapped[int]
