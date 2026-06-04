from starlette import status

from app.database.dependencies import SessionDep
from app.favourites.models.favorites import Favourite
from app.favourites.services import find_favourite
from fastapi import HTTPException

from app.services.tankerkoenig import get_specific_station
from app.users.dependencies import CurrentUser


async def create_favourite_station(
    station_id: str, current_user: CurrentUser, session: SessionDep
) -> Favourite:
    if await find_favourite(
        station_id=station_id, user_id=current_user.id, session=session
    ):
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This station is already in favourites",
        )
    station = await get_specific_station(station_id=station_id)
    new_favourite_station = Favourite(
        user_id=current_user.id,
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
