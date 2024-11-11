from typing import Union
from fastapi import FastAPI
from routers import general_objective_router, specific_objective_router, activity_router, task_router, week_router, schedule_router, project_router

app = FastAPI()

@app.get("/")
async def read_root():
    return {"End point de prueba": "proyecto de regalias"}

app.include_router(project_router.router, prefix="/api/v1", tags=["Projects"])
app.include_router(general_objective_router.router, prefix="/api/v1", tags=["General Objectives"])
app.include_router(specific_objective_router.router, prefix="/api/v1", tags=["Specific Objectives"])
app.include_router(activity_router.router, prefix="/api/v1", tags=["Activities"])
app.include_router(task_router.router, prefix="/api/v1", tags=["Tasks"])
app.include_router(week_router.router, prefix="/api/v1", tags=["Weeks"])
app.include_router(schedule_router.router, prefix="/api/v1", tags=["Schedules"])