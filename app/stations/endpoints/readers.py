from fastapi import APIRouter

from app.stations.schemes import StationsGetSchemes, StationsShowSchemes
from app.services.tankerkoenig import get_stations

router = APIRouter()


@router.post(path="/stations", response_model=list[StationsShowSchemes])
async def stations(data: StationsGetSchemes):
    res = await get_stations(data)
    return res


@router.post(path="/stations/best_stations", response_model=list[StationsShowSchemes])
async def best_stations(data: StationsGetSchemes):
    res = await get_stations(data)
    return res[:5]
