from fastapi import APIRouter

from app.schemes import StationsGetSchemes, StationsShowSchemes
from app.services.tankerkoenig import get_stations

router = APIRouter()

@router.post(path="/stations",response_model=list[StationsShowSchemes])
async def stations(data:StationsGetSchemes):
    res = await get_stations(data)
    if not res:
        return []
    return res