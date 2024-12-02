from fastapi import APIRouter, HTTPException
from typing import List
from services.counterpart_service import CounterpartService
from schemas.counterpart_schema import CounterpartSchema, CounterpartResponse

router = APIRouter()
service = CounterpartService()

@router.post("/counterparts", response_model=CounterpartResponse)
def create_counterpart(counterpart: CounterpartSchema):
    return service.create_counterpart(counterpart)

@router.get("/counterparts", response_model=List[CounterpartResponse])
def get_counterparts():
    return service.get_counterparts()

@router.get("/counterparts/{counterpart_id}", response_model=CounterpartResponse)
def get_counterpart_by_id(counterpart_id: int):
    counterpart = service.get_counterpart_by_id(counterpart_id)
    if counterpart is None:
        raise HTTPException(status_code=404, detail="Counterpart not found")
    return counterpart

@router.put("/counterparts/{counterpart_id}", response_model=CounterpartResponse)
def update_counterpart(counterpart_id: int, counterpart: CounterpartSchema):
    return service.update_counterpart(counterpart_id, counterpart)

@router.delete("/counterparts/{counterpart_id}", response_model=bool)
def delete_counterpart(counterpart_id: int):
    success = service.delete_counterpart(counterpart_id)
    if not success:
        raise HTTPException(status_code=404, detail="Counterpart not found")
    return success