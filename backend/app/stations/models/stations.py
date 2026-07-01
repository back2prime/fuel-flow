from decimal import Decimal
from datetime import datetime
from sqlalchemy import DateTime
from sqlalchemy import String, Numeric
from sqlalchemy.orm import mapped_column, Mapped
from app.enums import FuelType
from sqlalchemy import Index

from core.models.base import Base


class PriceHistory(Base):
    __tablename__ = "price_histories"

    station_id: Mapped[str] = mapped_column(String(36))
    fuel_type: Mapped[FuelType]
    price: Mapped[Decimal] = mapped_column(Numeric(precision=5, scale=3))
    recorded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))

    __table_args__ = (
        Index("ix_price_history_station_recorded", "station_id", "recorded_at"),
    )
