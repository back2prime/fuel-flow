from fastapi import FastAPI

from app.stations.endpoints.readers import stations_routers as st_router

app = FastAPI()

app.include_router(st_router)
