from fastapi import APIRouter, HTTPException
from typing import List
from services.schedule_service import ScheduleService
from schemas.schedule_schema import ScheduleCreate, ScheduleResponse

router = APIRouter()
service = ScheduleService()

@router.post("/schedules", response_model=ScheduleResponse)
def create_schedule(schedule: ScheduleCreate):
    return service.create_schedule(schedule)

@router.get("/schedules", response_model=List[ScheduleResponse])
def get_schedules():
    return service.get_schedules()

@router.get("/schedules/{id}", response_model=ScheduleResponse)
def get_schedule_by_id(id: int):
    schedule = service.get_schedule_by_id(id)
    if schedule is None:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return schedule

@router.get("/schedules/month/{month_id}", response_model=List[ScheduleResponse])
def get_schedules_by_month_id(month_id: int):
    schedules = service.get_schedules_by_month_id(month_id)
    if not schedules:
        raise HTTPException(status_code=404, detail="Schedules not found for month_id")
    return schedules

@router.get("/schedules/task/{task_id}", response_model=List[ScheduleResponse])
def get_schedules_by_task_id(task_id: int):
    schedules = service.get_schedules_by_task_id(task_id)
    if not schedules:
        raise HTTPException(status_code=404, detail="Schedules not found for task_id")
    return schedules

@router.put("/schedules/{id}", response_model=ScheduleResponse)
def update_schedule(id: int, schedule: ScheduleCreate):
    return service.update_schedule(id, schedule)

@router.delete("/schedules/{id}", response_model=bool)
def delete_schedule(id: int):
    success = service.delete_schedule(id)
    if not success:
        raise HTTPException(status_code=404, detail="Schedule not found")
    return success