from collections.abc import Sequence
from typing import Any
from uuid import UUID

from sqlalchemy import select, Result

from app.database.dependencies import SessionDep
from app.favourites.models.favorites import Favourite


async def find_favourite(
    station_id: str, user_id: UUID, session: SessionDep
) -> Any | None:
    stmt = select(Favourite.station_id).where(
        Favourite.station_id == station_id, Favourite.user_id == user_id
    )
    result: Result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def get_favourite_station_ids(
    user_id: UUID, session: SessionDep
) -> Sequence[str]:
    stmt = select(Favourite.station_id).where(Favourite.user_id == user_id)
    result: Result = await session.execute(stmt)
    return result.scalars().all()
