from pydantic import BaseModel, Field

from app.enums import FuelType, SortType


class StationShowBase(BaseModel):
    name: str
    address: str = Field(max_length=255)
    is_open: bool | None = Field(alias="isOpen")


class StationsGetSchemes(BaseModel):
    address: str = Field(max_length=255)
    radius: float = Field(le=25, serialization_alias="rad")
    fuel_type: FuelType = Field(serialization_alias="type")
    sort_type: SortType = Field(serialization_alias="sort")


class StationsShowSchemes(StationShowBase):
    id: str = Field(alias="id")
    distance_to: float = Field(alias="dist")
    fuel_price: float | None = Field(alias="price")


class StationShowInfo(StationShowBase):
    brand: str | None
    openingTimes: list[dict] | None
    overrides: list | None
    wholeDay: bool | None
