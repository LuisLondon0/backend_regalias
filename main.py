from typing import Union
from fastapi import FastAPI
from routers import general_objective_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"End point de prueba": "proyecto de regalias"}

app.include_router(general_objective_router.router, prefix="/api/v1", tags=["General Objectives"])