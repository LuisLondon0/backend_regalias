from typing import Union
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging
from database.database_pool import DatabasePool
import atexit

from routers import (
    month_router,
    specific_objective_router,
    activity_router,
    task_router,
    schedule_router,
    project_router,
    role_router,
    user_router,
    users_projects_router,
    fee_value_router,
    human_talent_router,
    annual_honorariums_router,
    equipment_software_router,
    counterpart_router,
    sgr_router
)

DatabasePool.initialize()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

@app.middleware("http")
async def custom_exception_handler(request, call_next):
    try:
        response = await call_next(request)
        return response
    except ValueError as e:
        return JSONResponse(status_code=400, content={"detail": str(e)})
    except HTTPException as e:
        return JSONResponse(status_code=e.status_code, content={"detail": e.detail})
    except Exception as e:
        logging.error(f"Unhandled exception: {e}")
        return JSONResponse(status_code=500, content={"detail": "Internal Server Error"})
    

@app.get("/")
async def read_root():
    return {"End point de prueba": "proyecto de regalias"}


app.include_router(role_router.router, prefix="/api/v1", tags=["Roles"])
app.include_router(user_router.router, prefix="/api/v1", tags=["Users"])
app.include_router(project_router.router, prefix="/api/v1", tags=["Projects"])
app.include_router(users_projects_router.router, prefix="/api/v1", tags=["Users Projects"])
app.include_router(specific_objective_router.router, prefix="/api/v1", tags=["Specific Objectives"])
app.include_router(activity_router.router, prefix="/api/v1", tags=["Activities"])
app.include_router(task_router.router, prefix="/api/v1", tags=["Tasks"])
app.include_router(month_router.router, prefix="/api/v1", tags=["Months"])
app.include_router(schedule_router.router, prefix="/api/v1", tags=["Schedules"])
app.include_router(fee_value_router.router, prefix="/api/v1", tags=["Fee Values"])
app.include_router(human_talent_router.router, prefix="/api/v1", tags=["Human Talents"])
app.include_router(annual_honorariums_router.router, prefix="/api/v1", tags=["Annual Honorariums"])
app.include_router(equipment_software_router.router, prefix="/api/v1", tags=["Equipment Softwares"])
app.include_router(counterpart_router.router, prefix="/api/v1", tags=["Counterparts"])
app.include_router(sgr_router.router, prefix="/api/v1", tags=["SGRs"])

atexit.register(DatabasePool.close_pool)