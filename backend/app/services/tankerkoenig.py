import json
from typing import Any

from fastapi import HTTPException
from pydantic import BaseModel

from app.enums import ResponseKey, CachePrefix, ApiMethod
from app.services.utils import (
    get_coords,
    edit_station_response,
    edit_stations_response,
)
from core.constants import REDIS_EXPIRE_SECONDS

from starlette import status

from core.utils import create_cache_key


class TankerkoenigService:
    """
    Service for fetching and caching gas station data from the Tankerkönig API.

    Implements cache-aside pattern: checks Redis before making HTTP requests.
    Cached responses expire after REDIS_EXPIRE_SECONDS.
    """

    def __init__(self, http_helper, redis_helper):
        self.http = http_helper
        self.redis = redis_helper

    async def get_http_response(
        self,
        params: dict[str, Any],
        method: ApiMethod,
        key: str,
        response_key: ResponseKey,
    ):
        try:
            api_response = await self.http.get_response(
                params=params, api_method=method
            )
            if not api_response["ok"]:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=api_response["message"],
                )
            data = api_response[response_key]
            if response_key == ResponseKey.STATIONS:
                edit_response = edit_stations_response(data)
            else:
                edit_response = [edit_station_response(data)]
            await self.redis.set(
                key=key, value=json.dumps(edit_response), ex=REDIS_EXPIRE_SECONDS
            )
            return edit_response
        except KeyError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Unexpected API response",
            )

    async def get_redis_response(
        self,
        obj: BaseModel,
        prefix: CachePrefix,
        method: ApiMethod,
        response_key: ResponseKey,
    ):
        stmt = obj.model_dump(mode="json", by_alias=True)
        if response_key == ResponseKey.STATIONS:
            stmt["lat"], stmt["lng"] = get_coords(stmt.pop("address"))
        key = create_cache_key(prefix=prefix, **stmt)
        redis_response = await self.redis.get(key=key)
        if redis_response:
            return json.loads(redis_response)
        return await self.get_http_response(
            params=stmt, method=method, key=key, response_key=response_key
        )
