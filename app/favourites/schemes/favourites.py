from pydantic import BaseModel, Field
from uuid import UUID


class FavouriteGetScheme(BaseModel):
    station_id: str
    user_id: UUID
