from fastapi import HTTPException


from app.stations.schemes import StationsGetSchemes
from app.services.utils import (
    get_coords,
    edit_station_response,
    check_response,
)
from core.helpers.http_helper import http_helper

from starlette import status

from core.helpers.redis_helper import redis_helper
from core.cache import create_cache_key


async def get_stations(obj: StationsGetSchemes) -> list[dict]:
    stmt = obj.model_dump(mode="json", by_alias=True)
    stmt["lat"], stmt["lng"] = get_coords(stmt.pop("address"))
    key = create_cache_key("stations", **stmt)
    redis_response = await redis_helper.get(key=key)

    return await check_response(
        response=redis_response, params=stmt, method="list.php", key=key
    )


async def get_specific_station(station_id: str) -> dict:
    stmt = {"id": station_id}
    try:
        response = await http_helper.get_response(params=stmt, api_method="detail.php")
        if not response["ok"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=response["message"]
            )
        return edit_station_response(response["station"])
    except KeyError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Unexpected API response"
        )
