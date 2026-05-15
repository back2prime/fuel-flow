from fastapi import FastAPI

from app.stations.endpoints.readers import router as fuel_router

app = FastAPI()

app.include_router(fuel_router)
