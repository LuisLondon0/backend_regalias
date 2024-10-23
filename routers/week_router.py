from fastapi import APIRouter, HTTPException
from typing import List
from services.week_service import WeekService
from schemas.week_schema import WeekCreate, WeekResponse

router = APIRouter()
service = WeekService()

@router.post("/weeks", response_model=WeekResponse)
def create_week(week: WeekCreate):
    try:
        return service.create_week(week)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/weeks", response_model=List[WeekResponse])
def get_weeks():
    try:
        return service.get_weeks()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/weeks/{week_id}", response_model=WeekResponse)
def get_week_by_id(week_id: int):
    try:
        week = service.get_week_by_id(week_id)
        if week is None:
            raise HTTPException(status_code=404, detail="Week not found")
        return week
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/weeks/{week_id}", response_model=WeekResponse)
def update_week(week_id: int, week: WeekCreate):
    try:
        return service.update_week(week_id, week)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/weeks/{week_id}", response_model=bool)
def delete_week(week_id: int):
    try:
        success = service.delete_week(week_id)
        if not success:
            raise HTTPException(status_code=404, detail="Week not found")
        return success
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")