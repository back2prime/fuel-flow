from fastapi import APIRouter

from app.stations.schemes import StationsGetSchemes, StationsShowSchemes
from app.services.tankerkoenig import get_stations, get_specific_station
from app.stations.schemes.stations import StationShowInfo

stations_routers = APIRouter()


@stations_routers.post(path="/stations", response_model=list[StationsShowSchemes])
async def get_best_stations(data: StationsGetSchemes, limit: int = None):
    res = await get_stations(data)
    return res[:limit] if limit else res


@stations_routers.post(path="/stations/{id}", response_model=StationShowInfo)
async def get_station(station_id: str):
    res = await get_specific_station(station_id)
    return res
