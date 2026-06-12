from typing import Optional
from uuid import UUID

from pydantic import Field, EmailStr, BaseModel, field_validator
from datetime import date

from core.schemes.base_scheme import FrozenModelType
from core.utils import password_strength_validator


class UserRegisterScheme(FrozenModelType):
    login: str = Field(max_length=50)
    email: EmailStr = Field(max_length=100)
    password: str
    name: str | None = Field(default=None, max_length=50)
    surname: str | None = Field(default=None, max_length=50)
    birth_date: date | None = Field(default=None)

    _validate_password = field_validator("password")(password_strength_validator)


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
    login: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = Field(default=None, max_length=100)
    name: Optional[str] = Field(default=None, max_length=50)
    surname: Optional[str] = Field(default=None, max_length=50)
    birth_date: Optional[date] = None

class UserPasswordPatchScheme(BaseModel):
    old_password: str = Field(examples=["MySecurePassword123!"])
    new_password: str = Field(examples=["MySecurePassword123!"])

    _validate_new_password = field_validator("new_password")(
        password_strength_validator
    )
