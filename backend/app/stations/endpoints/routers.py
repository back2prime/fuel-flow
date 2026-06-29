from fastapi import APIRouter, Query, Request

from app.enums import ApiMethod, ResponseKey, CachePrefix
from app.services.dependencies import TankerkoenigDep
from app.stations.schemes.stations import (
    StationsGetSchemes,
    StationGetScheme,
    StationsShowSchemes,
    StationShowInfo,
)
from core.helpers.limiter import limiter

stations_routers = APIRouter()


@stations_routers.post(
    path="/stations", tags=["Stations"], response_model=list[StationsShowSchemes]
)
@limiter.limit("5/minute")
async def get_best_stations(
    request: Request,
    data: StationsGetSchemes,
    service: TankerkoenigDep,
    limit: int = Query(default=10, ge=1, le=50),
):
    res = await service.get_redis_response(
        obj=data,
        prefix=CachePrefix.STATIONS,
        method=ApiMethod.STATIONS,
        response_key=ResponseKey.STATIONS,
    )
    return res[:limit] if limit else res


@stations_routers.post(
    path="/stations/{station_id}", tags=["Stations"], response_model=StationShowInfo
)
@limiter.limit("5/minute")
async def get_station(request: Request, station_id: str, service: TankerkoenigDep):
    res = await service.get_redis_response(
        obj=StationGetScheme(id=station_id),
        prefix=CachePrefix.STATION,
        method=ApiMethod.STATION,
        response_key=ResponseKey.STATION,
    )
    return res[0]
