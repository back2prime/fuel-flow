import httpx

from config import settings
from app.schemes import StationsGetSchemes
from app.services.utils import get_coords, edit_response

BASE_URL = "https://creativecommons.tankerkoenig.de/json"

async def get_stations(obj: StationsGetSchemes) -> list:
    url = f"{BASE_URL}/list.php"
    lat,lng = get_coords(obj)

    params = {
        "lat": lat,
        "lng": lng,
        "rad": obj.radius,
        "type": "all",
        "apikey": settings.API_KEY,
    }

    async with httpx.AsyncClient() as client:
        response = await client.get(url,params=params)

    return edit_response(response.json()["stations"])
