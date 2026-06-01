from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String

from typing import TYPE_CHECKING

from core.models.base import Base

if TYPE_CHECKING:
    from app.prices.models.price import Price
    from app.stations.models.favorites import Favourite


class Station(Base):
    """Gas station with address and associated prices."""

    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] = mapped_column(String(255))
    prices: Mapped[list["Price"]] = relationship(
        argument="Price", back_populates="station"
    )
    favourites: Mapped[list["Favourite"]] = relationship(
        argument="Favourite", back_populates="station"
    )
