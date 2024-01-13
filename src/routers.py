from fastapi import APIRouter

from src.bookings.router import router as bookings_router
from src.hotels.rooms.router import router as rooms_router
from src.hotels.router import router as hotels_router
from src.users.router import router as users_router

api_router = APIRouter()

api_router.include_router(router=users_router)
api_router.include_router(router=bookings_router)
api_router.include_router(router=hotels_router)
api_router.include_router(router=rooms_router)
