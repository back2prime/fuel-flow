from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey

from core.base import Base

from uuid import UUID

class Station(Base):

    name: Mapped[str]
    address: Mapped[str]
    prices = relationship(argument="Price",back_populates="station")

class Price(Base):

    station_id: Mapped[UUID] = mapped_column(ForeignKey("stations.id"))
    diesel: Mapped[float | None]
    e5: Mapped[float | None]
    e10: Mapped[float | None]
    station = relationship(argument="Station",back_populates="prices")

