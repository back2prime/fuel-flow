from typing import TYPE_CHECKING

from uuid import UUID
from sqlalchemy import ForeignKey, UniqueConstraint

from core.models.base import Base

from sqlalchemy.orm import Mapped, relationship, mapped_column

if TYPE_CHECKING:
    from app.users.models.users import User


class Favourite(Base):
    """Association table linking users to their favourite stations."""

    user_id: Mapped[UUID] = mapped_column(ForeignKey("users.id"))
    station_id: Mapped[str]

    __table_args__ = (
        UniqueConstraint("user_id", "station_id", name="uq_user_station"),
    )

    user: Mapped["User"] = relationship(argument="User", back_populates="favourites")
