from pydantic import BaseModel, Field


class FavouriteGetScheme(BaseModel):
    name: str
    address: str = Field(max_length=255)
    is_open: bool | None = Field(serialization_alias="isOpen")
    brand: str | None
    openingTimes: list[dict] | None
    overrides: list | None
    wholeDay: bool | None
