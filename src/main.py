import time
from contextlib import asynccontextmanager

import sentry_sdk
import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis.utils import from_url
from sentry_sdk.integrations.fastapi import FastApiIntegration
from sentry_sdk.integrations.starlette import StarletteIntegration
from sqladmin import Admin

from config import settings
from src import routers
from src.admin.auth import authentication_backend
from src.admin.views import BookingsAdmin, HotelsAdmin, RoomsAdmin, UsersAdmin
from src.database import engine
from src.logger import init_logging, logger

init_logging()

sentry_sdk.init(
    dsn=settings.sentry_dsn,
    traces_sample_rate=1.0,
    profiles_sample_rate=1.0,
    enable_tracing=True,
    integrations=[
        StarletteIntegration(transaction_style="url"),
        FastApiIntegration(transaction_style="url"),
    ],
)


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa
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


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    logger.info(f"Process time for url {request.url}: {process_time}")
    return response


app.add_middleware(
    middleware_class=CORSMiddleware,  # noqa
    allow_origins=settings.origins,
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
