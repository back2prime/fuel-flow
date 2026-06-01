from typing import Optional
from uuid import UUID

from pydantic import Field, EmailStr, BaseModel
from datetime import date

from core.schemes.base_scheme import FrozenModelType


class UserRegisterScheme(FrozenModelType):
    login: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str
    name: str | None = Field(default=None, max_length=50)
    surname: str | None = Field(default=None, max_length=50)
    birth_date: date | None


class UserGetScheme(BaseModel):
    id: UUID
    login: str
    email: EmailStr
    name: str | None
    surname: str | None
    birth_date: date | None


class UserLoginScheme(FrozenModelType):
    login: str = Field(max_length=50)
    password: str


class UserPatchScheme(BaseModel):
    login: Optional[str] = None
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    surname: Optional[str] = None
    birth_date: Optional[date] = None


class UserPasswordPatchScheme(BaseModel):
    old_password: str
    new_password: str
