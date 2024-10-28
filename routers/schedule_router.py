from fastapi import APIRouter, HTTPException
from typing import List
from services.schedule_service import ScheduleService
from schemas.schedule_schema import ScheduleCreate, ScheduleTaskResponse

router = APIRouter()
service = ScheduleService()

@router.post("/schedules", response_model=ScheduleTaskResponse)
def create_schedule(schedule: ScheduleCreate):
    try:
        return service.create_schedule(schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/schedules", response_model=List[ScheduleTaskResponse])
def get_schedules():
    try:
        return service.get_schedules()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/schedules/{schedule_id}", response_model=ScheduleTaskResponse)
def get_schedule_by_id(schedule_id: int):
    try:
        schedule = service.get_schedule_by_id(schedule_id)
        if schedule is None:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return schedule
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/schedules/{schedule_id}", response_model=ScheduleTaskResponse)
def update_schedule(schedule_id: int, schedule: ScheduleCreate):
    try:
        return service.update_schedule(schedule_id, schedule)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/schedules/{schedule_id}", response_model=bool)
def delete_schedule(schedule_id: int):
    try:
        success = service.delete_schedule(schedule_id)
        if not success:
            raise HTTPException(status_code=404, detail="Schedule not found")
        return success
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")