from datetime import date

import bcrypt
from sqlalchemy.orm import Mapped, relationship, mapped_column
from sqlalchemy import String, Date

from core import settings
from core.models.base import Base


class User(Base):
    login: Mapped[str] = mapped_column(String(50), unique=True)
    email: Mapped[str] = mapped_column(String(100), unique=True)
    password_hash: Mapped[str] = mapped_column(String(255))

    name: Mapped[str | None]
    surname: Mapped[str | None]
    birth_date: Mapped[date | None]

    @staticmethod
    def generate_password_hash(password: str) -> str:
        salt: bytes = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(settings.encoding), salt).decode(
            settings.encoding
        )

    def set_password(self, password: str) -> None:
        """Генерация пароля"""
        self.password_hash = self.generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        """Проверка пароля"""
        return bcrypt.checkpw(
            password.encode(settings.encoding),
            self.password_hash.encode(settings.encoding),
        )
