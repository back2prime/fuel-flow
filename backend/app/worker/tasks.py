from app.worker.utils import get_station_id, fetch_station_prices, build_price_records
from core.helpers.celery_helper import celery_helper
from core.helpers.db_helper import db_helper


@celery_helper.task
def collect_station_prices():
    with db_helper.sync_session_factory() as session:
        station_ids = get_station_id()
        for station in station_ids:
            prices = fetch_station_prices(station_id=station)
            records = build_price_records(station_id=station, prices=prices)
            session.add_all(records)
        session.commit()
