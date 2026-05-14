from sqlalchemy.orm import Mapped, relationship,mapped_column
from sqlalchemy import String

from core.models.base import Base


class Station(Base):

    name: Mapped[str] = mapped_column(String(50))
    address: Mapped[str] =  mapped_column(String(255))
    prices = relationship(argument="Price", back_populates="station")
