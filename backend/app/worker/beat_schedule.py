from datetime import timedelta

from core.helpers.celery_helper import celery_helper

celery_helper.conf.beat_schedule = {
    "collect-station-prices": {
        "task": "app.worker.tasks.collect_station_prices",
        "schedule": timedelta(minutes=30),
    }
}
