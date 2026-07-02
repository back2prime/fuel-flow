import httpx
from sqlalchemy import select, Sequence
from datetime import datetime, UTC
from app.enums import ApiMethod, ResponseKey, FuelType
from app.stations.models.stations import PriceHistory
from core.constants import HTTP_URL
from core.config import settings

from core.helpers.db_helper import db_helper
from app.favourites.models.favorites import Favourite
from app.users.models.users import User  # noqa: F401


def get_station_id() -> Sequence[str]:
    stmt = select(Favourite.station_id).distinct()
    with db_helper.sync_session_factory() as session:
        return session.scalars(stmt).all()


def fetch_station_prices(station_id: str) -> dict:
    url = f"{HTTP_URL}{ApiMethod.STATION.value}?id={station_id}&apikey={settings.api.API_KEY}"
    response = httpx.get(url=url).json()
    if not response["ok"]:
        raise ValueError(
            f"Tankerkönig API error for station {station_id}: {response.get('message', 'unknown error')}"
        )
    prices = {}
    for field in response[ResponseKey.STATION]:
        if field in FuelType:
            prices[field] = response[ResponseKey.STATION][field]
    return prices


def build_price_records(station_id: str, prices: dict) -> list[PriceHistory]:
    result = []
    for fuel_type, price in prices.items():
        item = PriceHistory(
            station_id=station_id,
            fuel_type=fuel_type,
            price=price,
            recorded_at=datetime.now(UTC),
        )
        result.append(item)
    return result
