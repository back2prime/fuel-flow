"""Celery application instance for fuel-flow background workers."""

from celery import Celery

from core.config import settings

celery_helper = Celery(
    name="fuel-flow", broker=settings.redis.url, include=["app.worker.tasks"]
)

celery_helper.conf.update(
    result_backend=settings.redis.url,
    timezone="UTC",
    enable_utc=True,
)

import app.worker.beat_schedule  # noqa: E402
