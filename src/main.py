import uvicorn
from fastapi import FastAPI

from src import routers

app = FastAPI(
    title="PyBooking",
    summary="Бронирование отелей",
    description="Пример проекта на FastAPI по поиску и бронированию отелей.",
    version="0.1.0",
)


app.include_router(routers.api_router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)
