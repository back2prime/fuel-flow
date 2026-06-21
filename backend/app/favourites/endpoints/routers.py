from collections.abc import Sequence

from fastapi import APIRouter


from app.database.dependencies import SessionDep
from app.favourites.crud import create_favourite_station, delete_favourite_station
from app.favourites.models.favorites import Favourite
from app.favourites.schemes.favourites import FavouriteGetScheme
from app.favourites.services import get_favourites_by_user_id
from app.services.dependencies import TankerkoenigDep
from app.users.dependencies import CurrentUser
from core.schemes.common import StatusScheme

favourites_routers = APIRouter()


@favourites_routers.post(
    path="/stations/{station_id}/favourite",
    tags=["Favourites"],
    response_model=FavouriteGetScheme,
)
async def add_favourite(
    station_id: str,
    current_user: CurrentUser,
    session: SessionDep,
    service: TankerkoenigDep,
) -> Favourite:
    return await create_favourite_station(
        station_id=station_id, user_id=current_user.id, session=session, service=service
    )


@favourites_routers.get(
    path="/users/me/favourites",
    tags=["Favourites"],
    response_model=list[FavouriteGetScheme],
)
async def get_favourites(
    current_user: CurrentUser, session: SessionDep
) -> Sequence[Favourite]:
    return await get_favourites_by_user_id(user_id=current_user.id, session=session)


@favourites_routers.delete(
    path="/stations/{station_id}/favourite",
    tags=["Favourites"],
    response_model=StatusScheme,
)
async def remove_favourite(
    current_user: CurrentUser, station_id: str, session: SessionDep
) -> dict:
    return await delete_favourite_station(
        user_id=current_user.id, station_id=station_id, session=session
    )
