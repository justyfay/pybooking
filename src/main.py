from contextlib import asynccontextmanager
from typing import List

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from loguru import logger
from redis.utils import from_url
from sqladmin import Admin

from config import settings
from src import routers
from src.admin.auth import authentication_backend
from src.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from src.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    redis = from_url(settings.redis_url, encoding="utf-8", decode_responses=True)
    FastAPICache.init(RedisBackend(redis), prefix="cache")

    logger.info(f"Service cache started: {settings.redis_url}")
    yield
    logger.info(f"Service cache exited: {settings.redis_url}")


app: FastAPI = FastAPI(
    title="PyBooking",
    summary="Бронирование отелей",
    description="Пример проекта на FastAPI по поиску и бронированию отелей.",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(routers.api_router)
app.mount("/src/static", StaticFiles(directory="src/static"), "static")

admin = Admin(app, engine, authentication_backend=authentication_backend)
admin.add_view(UsersAdmin)
admin.add_view(HotelsAdmin)
admin.add_view(RoomsAdmin)
admin.add_view(BookingsAdmin)

origins: List[str] = ["http://localhost:8000", "http://localhost:3000"]

app.add_middleware(
    middleware_class=CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=[
        "Content-Type",
        "Set-Cookie",
        "Access-Control-Allow-Headers",
        "Access-Control-Allow-Origin",
        "Authorization",
    ],
)

if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
