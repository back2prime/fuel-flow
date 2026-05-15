from pydantic import BaseModel, Field

from app.emuns import FuelType, SortType


class StationsGetSchemes(BaseModel):
    address: str = Field(max_length=255)
    radius: float = Field(le=25)
    fuel_type: FuelType
    sort_type: SortType


class StationsShowSchemes(BaseModel):
    name: str
    address: str
    distance_to: float = Field(alias="dist")
    is_open: bool = Field(alias="isOpen")
    fuel_price: float | None = Field(alias="price")
