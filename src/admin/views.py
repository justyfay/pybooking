from sqladmin import ModelView

from src.bookings.models import Bookings
from src.hotels.models import Hotels
from src.hotels.rooms.models import Rooms
from src.users.models import Users


class UsersAdmin(ModelView, model=Users):
    column_list = [Users.id, Users.email, Users.bookings]
    column_details_exclude_list = [Users.hashed_password]
    name = "Users"
    name_plural = "Users"
    can_delete = False
    icon = "fa-solid fa-user"


class HotelsAdmin(ModelView, model=Hotels):
    column_list = [c.name for c in Hotels.__table__.c] + [Hotels.rooms]
    name = "Hotels"
    name_plural = "Hotels"
    icon = "fa-solid fa-hotel"


class RoomsAdmin(ModelView, model=Rooms):
    column_list = [c.name for c in Rooms.__table__.c] + [Rooms.hotel, Rooms.bookings]
    name = "Rooms"
    name_plural = "Rooms"
    icon = "fa-solid fa-bed"


class BookingsAdmin(ModelView, model=Bookings):
    column_list = [c.name for c in Bookings.__table__.c] + [
        Bookings.user,
        Bookings.room,
    ]
    name = "Bookings"
    name_plural = "Bookings"
    icon = "fa-solid fa-book"
    can_delete = False
