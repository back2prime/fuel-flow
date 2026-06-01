from uuid import UUID

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base

if TYPE_CHECKING:
    from app.stations.models.stations import Station


class Price(Base):
    """Fuel prices for a station."""

    station_id: Mapped[UUID] = mapped_column(ForeignKey("stations.id"))
    diesel: Mapped[float | None]
    e5: Mapped[float | None]
    e10: Mapped[float | None]
    station: Mapped["Station"] = relationship(
        argument="Station", back_populates="prices"
    )
