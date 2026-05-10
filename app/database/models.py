from sqlalchemy.orm import Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey

from core.base import Base

from uuid import UUID

class StationModel(Base):

    name: Mapped[str]
    address: Mapped[str]
    prices = relationship(argument="PricesModel",back_populates="station")

class PriceModel(Base):

    station_id: Mapped[UUID] = mapped_column(ForeignKey("stations.id"))
    diesel: Mapped[float]
    e5: Mapped[float]
    e10: Mapped[float]
    station = relationship(argument="StationsModel",back_populates="prices")

