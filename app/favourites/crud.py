from starlette import status

from app.database.dependencies import SessionDep
from app.favourites.models.favorites import Favourite
from app.favourites.services import find_favourite
from fastapi import HTTPException

from app.users.dependencies import CurrentUser


async def create_favourite_station(
    station_id: str, current_user: CurrentUser, session: SessionDep
) -> Favourite:
    response = await find_favourite(
        station_id=station_id, user_id=current_user.id, session=session
    )
    if response.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="This station is already in favourites",
        )

    new_favourite_station = Favourite(user_id=current_user.id, station_id=station_id)
    session.add(new_favourite_station)
    await session.commit()
    await session.refresh(new_favourite_station)
    return new_favourite_station
