from fastapi import APIRouter

from app.database.dependencies import SessionDep
from app.favourites.crud import create_favourite_station
from app.favourites.models.favorites import Favourite
from app.favourites.schemes.favourites import FavouriteGetScheme
from app.stations.schemes.stations import StationsShowSchemes
from app.users.dependencies import CurrentUser

favourites_routers = APIRouter()


@favourites_routers.post(
    path="/stations/{station_id}/favourite",
    tags=["Favourites"],
    response_model=FavouriteGetScheme,
)
async def add_favourite(
    station_id: str, current_user: CurrentUser, session: SessionDep
) -> Favourite:
    return await create_favourite_station(
        station_id=station_id, current_user=current_user, session=session
    )


@favourites_routers.get(
    path="/users/me/favourites",
    tags=["Favourites"],
    response_model=list[StationsShowSchemes],
)
async def get_favourites(current_user: CurrentUser, session: SessionDep):
    pass
