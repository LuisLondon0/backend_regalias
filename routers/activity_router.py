from fastapi import APIRouter, HTTPException
from typing import List
from services.activity_service import ActivityService
from schemas.activity_schema import ActivityCreate, ActivityResponse

router = APIRouter()
service = ActivityService()

@router.post("/activities", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate):
    try:
        return service.create_activity(activity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/activities", response_model=List[ActivityResponse])
def get_activities():
    try:
        return service.get_activities()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity_by_id(activity_id: int):
    try:
        activity = service.get_activity_by_id(activity_id)
        if activity is None:
            raise HTTPException(status_code=404, detail="Activity not found")
        return activity
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, activity: ActivityCreate):
    try:
        return service.update_activity(activity_id, activity)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/activities/{activity_id}", response_model=bool)
def delete_activity(activity_id: int):
    try:
        success = service.delete_activity(activity_id)
        if not success:
            raise HTTPException(status_code=404, detail="Activity not found")
        return success
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")