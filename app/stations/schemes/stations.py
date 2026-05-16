from pydantic import BaseModel, Field

from app.enums import FuelType, SortType


class StationsGetSchemes(BaseModel):
    address: str = Field(max_length=255)
    radius: float = Field(le=25, serialization_alias="rad")
    fuel_type: FuelType = Field(serialization_alias="type")
    sort_type: SortType = Field(serialization_alias="sort")


class StationsShowSchemes(BaseModel):
    name: str
    address: str
    distance_to: float = Field(alias="dist")
    is_open: bool = Field(alias="isOpen")
    fuel_price: float | None = Field(alias="price")
