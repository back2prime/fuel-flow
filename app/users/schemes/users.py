from pydantic import Field, EmailStr
from datetime import date

from core.scheme import FrozenModelType


class Registration(FrozenModelType):
    login: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str
    name: str | None = Field(default=None, max_length=50)
    surname: str | None = Field(default=None, max_length=50)
    birth_date: date | None
