import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src import routers

app = FastAPI(
    title="PyBooking",
    summary="Бронирование отелей",
    description="Пример проекта на FastAPI по поиску и бронированию отелей.",
    version="0.1.0",
)

app.include_router(routers.api_router)
app.mount("/src/static", StaticFiles(directory="src/static"), "static")

origins = ["http://localhost:8000", "http://localhost:3000"]

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
