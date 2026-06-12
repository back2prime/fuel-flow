from datetime import date
from typing import TYPE_CHECKING


import bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

from core.config import settings
from core.models.base import Base

if TYPE_CHECKING:
    from app.favourites.models.favorites import Favourite


class User(Base):
    """User model with authentication and profile fields."""

    login: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    name: Mapped[str | None] = mapped_column(String(50))
    surname: Mapped[str | None] = mapped_column(String(50))
    birth_date: Mapped[date | None]

    favourites: Mapped[list["Favourite"]] = relationship(
        argument="Favourite", back_populates="user"
    )

    @staticmethod
    def generate_password_hash(password: str) -> str:
        salt: bytes = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(settings.encoding), salt).decode(
            settings.encoding
        )

    def set_password(self, password: str) -> None:
        """Hash and set user password"""
        self.password_hash = self.generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Verify password against stored hash"""
        return bcrypt.checkpw(
            password.encode(settings.encoding),
            self.password_hash.encode(settings.encoding),
        )
