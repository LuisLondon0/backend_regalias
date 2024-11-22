from fastapi import APIRouter, HTTPException
from typing import List
from services.month_service import MonthService
from schemas.month_schema import MonthCreate, MonthResponse

router = APIRouter()
service = MonthService()

@router.post("/months", response_model=MonthResponse)
def create_month(month: MonthCreate):
    return service.create_month(month)

@router.get("/months", response_model=List[MonthResponse])
def get_months():
    return service.get_months()

@router.get("/months/{month_id}", response_model=MonthResponse)
def get_month_by_id(month_id: int):
    month = service.get_month_by_id(month_id)
    if month is None:
        raise HTTPException(status_code=404, detail="Month not found")
    return month

@router.put("/months/{month_id}", response_model=MonthResponse)
def update_month(month_id: int, month: MonthCreate):
    return service.update_month(month_id, month)

@router.delete("/months/{month_id}", response_model=bool)
def delete_month(month_id: int):
    success = service.delete_month(month_id)
    if not success:
        raise HTTPException(status_code=404, detail="Month not found")
    return success