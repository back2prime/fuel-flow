from typing import TYPE_CHECKING

from uuid import UUID
from sqlalchemy import ForeignKey, UniqueConstraint

from core.models.base import Base

from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from app.users.models.users import User
    from app.stations.models.stations import Station


class Favourite(Base):
    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    station_id: Mapped[UUID] = mapped_column(ForeignKey("stations.id"))

    __table_args__ = (
        UniqueConstraint("user_id", "station_id", name="uq_user_station"),
    )

    user: Mapped["User"] = relationship(argument="User", back_populates="favourites")
    station: Mapped["Station"] = relationship(
        argument="Station", back_populates="favourites"
    )
