from fastapi import APIRouter, HTTPException
from typing import List
from services.activity_service import ActivityService
from schemas.activity_schema import ActivityCreate, ActivityResponse

router = APIRouter()
service = ActivityService()

@router.post("/activities", response_model=ActivityResponse)
def create_activity(activity: ActivityCreate):
    return service.create_activity(activity)

@router.get("/activities", response_model=List[ActivityResponse])
def get_activities():
    return service.get_activities()

@router.get("/activities/{activity_id}", response_model=ActivityResponse)
def get_activity_by_id(activity_id: int):
    activity = service.get_activity_by_id(activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")
    return activity

@router.put("/activities/{activity_id}", response_model=ActivityResponse)
def update_activity(activity_id: int, activity: ActivityCreate):
    return service.update_activity(activity_id, activity)

@router.delete("/activities/{activity_id}", response_model=bool)
def delete_activity(activity_id: int):
    success = service.delete_activity(activity_id)
    if not success:
        raise HTTPException(status_code=404, detail="Activity not found")
    return success