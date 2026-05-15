from uuid import UUID

from sqlalchemy import ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from core.models.base import Base


class Price(Base):

    station_id: Mapped[UUID] = mapped_column(ForeignKey("stations.id"))
    diesel: Mapped[float | None]
    e5: Mapped[float | None]
    e10: Mapped[float | None]
    station = relationship(argument="Station", back_populates="prices")
