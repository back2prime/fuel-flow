import json
from typing import Any

from fastapi import HTTPException
from geopy.geocoders import Nominatim
from starlette import status

from core.helpers import http_helper, redis_helper

geolocator = Nominatim(user_agent="my_app")


def get_coords(address: str) -> tuple:
    location = geolocator.geocode(address)
    return round(location.latitude, 3), round(location.longitude, 3)


def edit_address(response: dict) -> dict:
    address = (
        f"{response.pop('postCode', '')} {response.pop('place', '')}"
        f" {response.pop('street', '')} {response.pop('houseNumber','')}"
    )
    response["address"] = address
    return response


def edit_stations_response(response: list[dict]) -> list[dict]:
    result = []
    for station in response:
        if station["isOpen"] and station["price"]:
            edit_address(station)
            result.append(station)
    return result


def edit_station_response(response: dict) -> dict:
    return edit_address(response)


def create_cache_key(prefix: str, **kwargs) -> str:
    values = ":".join(str(v) for v in kwargs.values())
    return f"{prefix}:{values}"


async def check_response(
    response: str | None, params: dict[str, Any], method: str, key: str
) -> list[dict]:
    if not response:
        try:
            api_response = await http_helper.get_response(
                params=params, api_method=method
            )
            if not api_response["ok"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=api_response["message"],
                )
            edit_response = edit_stations_response(api_response["stations"])
            await redis_helper.set(key=key, value=json.dumps(edit_response), ex=1800)
            return edit_response
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unexpected API response",
            )
    else:
        return json.loads(response)
