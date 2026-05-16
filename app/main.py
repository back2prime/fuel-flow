from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.stations.endpoints.readers import stations_routers as st_router
from core.http_helper import http_helper


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await http_helper.close()


app = FastAPI(lifespan=lifespan)

app.include_router(st_router)
