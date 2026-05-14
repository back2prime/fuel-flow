from sqlalchemy.orm import Mapped, relationship

from core.models.base import Base


class Station(Base):

    name: Mapped[str]
    address: Mapped[str]
    prices = relationship(argument="Price", back_populates="station")
