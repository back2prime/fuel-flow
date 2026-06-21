from starlette import status
from uuid import UUID

from app.database.dependencies import SessionDep
from app.enums import CachePrefix, ApiMethod, ResponseKey
from app.favourites.models.favorites import Favourite
from app.favourites.services import find_favourite
from fastapi import HTTPException

from app.services.dependencies import TankerkoenigDep
from app.stations.schemes.stations import StationGetScheme


async def create_favourite_station(
    station_id: str, user_id: UUID, session: SessionDep, service: TankerkoenigDep
) -> Favourite:
    if await find_favourite(station_id=station_id, user_id=user_id, session=session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This station is already in favourites",
        )
    station = await service.get_redis_response(
        obj=StationGetScheme(id=station_id),
        prefix=CachePrefix.STATION,
        method=ApiMethod.STATION,
        response_key=ResponseKey.STATION,
    )
    station = station[0]
    new_favourite_station = Favourite(
        user_id=user_id,
        station_id=station_id,
        name=station["name"],
        address=station["address"],
        brand=station["brand"],
        openingTimes=station["openingTimes"],
        overrides=station["overrides"],
        wholeDay=station["wholeDay"],
    )
    session.add(new_favourite_station)
    await session.commit()
    await session.refresh(new_favourite_station)
    return new_favourite_station


async def delete_favourite_station(
    user_id: UUID, station_id: str, session: SessionDep
) -> dict:
    station = await find_favourite(
        station_id=station_id, user_id=user_id, session=session
    )
    if not station:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Station not found",
        )
    await session.delete(station)
    await session.commit()
    return {"status": "ok"}
