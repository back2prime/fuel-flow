import asyncio

from app.database.connect_db import engine
from app.database.models import Base

from app.database.models import StationsModel


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

asyncio.run(init_models())

