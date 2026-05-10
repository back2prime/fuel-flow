from pydantic import BaseModel, Field
from uuid import UUID

class StationsGetSchemes(BaseModel):
    address: str = Field(max_length=50)
    radius: float = Field(le=25)

class StationsShowSchemes(BaseModel):
    station_id: UUID = Field(alias="id")
    name: str
    address: str
    distance_to: float = Field(alias="dist")
    is_open: bool = Field(alias="isOpen")
    diesel: float | None = None
    e5: float | None = None
    e10: float | None = None
