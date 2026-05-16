from fastapi import APIRouter

from app.stations.schemes import StationsGetSchemes, StationsShowSchemes
from app.services.tankerkoenig import get_stations

stations_routers  = APIRouter()


@stations_routers.post(path="/stations", response_model=list[StationsShowSchemes])
async def get_best_stations(data: StationsGetSchemes,limit: int = None):
    res = await get_stations(data)
    return res[:limit] if limit else res


