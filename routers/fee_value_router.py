from fastapi import APIRouter, HTTPException
from typing import List
from services.fee_value_service import FeeValueService
from schemas.fee_value_schema import FeeValueCreate, FeeValueResponse

router = APIRouter()
service = FeeValueService()

@router.post("/fee_values", response_model=FeeValueResponse)
def create_fee_value(fee_value: FeeValueCreate):
    return service.create_fee_value(fee_value)

@router.get("/fee_values", response_model=List[FeeValueResponse])
def get_fee_values():
    return service.get_fee_values()

@router.get("/fee_values/{fee_value_id}", response_model=FeeValueResponse)
def get_fee_value_by_id(fee_value_id: int):
    fee_value = service.get_fee_value_by_id(fee_value_id)
    if fee_value is None:
        raise HTTPException(status_code=404, detail="Fee value not found")
    return fee_value

@router.put("/fee_values/{fee_value_id}", response_model=FeeValueResponse)
def update_fee_value(fee_value_id: int, fee_value: FeeValueCreate):
    return service.update_fee_value(fee_value_id, fee_value)

@router.delete("/fee_values/{fee_value_id}", response_model=bool)
def delete_fee_value(fee_value_id: int):
    success = service.delete_fee_value(fee_value_id)
    if not success:
        raise HTTPException(status_code=404, detail="Fee value not found")
    return success