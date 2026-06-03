from uuid import UUID

from sqlalchemy import select, Result

from app.database.dependencies import SessionDep
from app.favourites.models.favorites import Favourite


async def find_favourite(station_id: str, user_id: UUID, session: SessionDep) -> Result:
    stmt = select(Favourite.station_id).where(
        Favourite.station_id == station_id, Favourite.user_id == user_id
    )
    result: Result = await session.execute(stmt)
    return result
