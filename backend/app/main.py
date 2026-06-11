from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.favourites.endpoints.routers import favourites_routers as fav_router
from app.stations.endpoints.routers import stations_routers as st_router
from app.users.endpoints.routers import user_routers as ur_router
from core.helpers.http_helper import http_helper
from core.helpers.redis_helper import redis_helper

from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await http_helper.close()
    await redis_helper.close()


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(st_router)
app.include_router(ur_router)
app.include_router(fav_router)
