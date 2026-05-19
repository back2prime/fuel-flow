from fastapi import HTTPException

import json

from app.stations.schemes import StationsGetSchemes
from app.services.utils import get_coords, edit_stations_response, edit_station_response
from core.http_helper import http_helper

from starlette import status

from core.redis_helper import redis_helper
from app.services.utils import create_redis_key


async def get_stations(obj: StationsGetSchemes) -> list[dict]:
    stmt = obj.model_dump(mode="json", by_alias=True)
    stmt["lat"], stmt["lng"] = get_coords(stmt.pop("address"))
    key = create_redis_key(obj, stmt["lat"], stmt["lng"])
    redis_response = await redis_helper.get(key=key)

    if not redis_response:
        try:
            response = await http_helper.get_response(
                params=stmt, api_method="list.php"
            )
            if not response["ok"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST, detail=response["message"]
                )
            edit_response = edit_stations_response(response["stations"])
            await redis_helper.set(key=key, value=json.dumps(edit_response), ex=1800)
            return edit_response
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unexpected API response",
            )
    else:
        return json.loads(redis_response)


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
