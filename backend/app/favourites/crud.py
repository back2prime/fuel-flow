from starlette import status
from uuid import UUID

from app.database.dependencies import SessionDep
from app.favourites.models.favorites import Favourite
from app.favourites.services import find_favourite
from fastapi import HTTPException

from app.services.tankerkoenig import get_specific_station


async def create_favourite_station(
    station_id: str, user_id: UUID, session: SessionDep
) -> Favourite:
    if await find_favourite(station_id=station_id, user_id=user_id, session=session):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This station is already in favourites",
        )
    station = await get_specific_station(station_id=station_id)
    new_favourite_station = Favourite(
        user_id=user_id,
        station_id=station_id,
        name=station["name"],
        address=station["address"],
        is_open=station["isOpen"],
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
