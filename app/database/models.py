from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,relationship
from sqlalchemy import ForeignKey

from uuid import UUID


class Base(DeclarativeBase):
    id: Mapped[UUID] = mapped_column(primary_key=True)

class StationsModel(Base):
    __tablename__ = "stations"

    name: Mapped[str]
    address: Mapped[str]
    prices = relationship(argument="PricesModel",back_populates="station")

class PricesModel(Base):
    __tablename__ = "prices"

    station_id: Mapped[UUID] = mapped_column(ForeignKey("stations.id"))
    diesel: Mapped[float]
    e5: Mapped[float]
    e10: Mapped[float]
    station = relationship(argument="StationsModel",back_populates="prices")

