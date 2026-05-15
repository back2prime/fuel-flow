import httpx

from core.config import settings
from app.stations.schemes import StationsGetSchemes
from app.services.utils import get_coords, edit_response

BASE_URL = "https://creativecommons.tankerkoenig.de/json"


async def get_stations(obj: StationsGetSchemes) -> list:
    url = f"{BASE_URL}/list.php"
    lat, lng = get_coords(obj)

    params = {
        "lat": lat,
        "lng": lng,
        "rad": obj.radius,
        "type": obj.fuel_type.value,
        "sort": obj.sort_type.value,
        "apikey": settings.API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url, params=params)

    return edit_response(response.json()["stations"])
