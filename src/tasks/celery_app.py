from celery import Celery

from config import settings

celery: Celery = Celery(
    name="tasks",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include="src.tasks.tasks",
)
