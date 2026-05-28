from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.stations.endpoints.readers import stations_routers as st_router
from app.users.endpoints.routers import user_routers as ur_router
from core.helpers.http_helper import http_helper
from core.helpers.redis_helper import redis_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await http_helper.close()
    await redis_helper.close()


app = FastAPI(lifespan=lifespan)

app.include_router(st_router)
app.include_router(ur_router)
