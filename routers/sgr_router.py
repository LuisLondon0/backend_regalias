from fastapi import APIRouter, HTTPException
from typing import List
from services.sgr_service import SGRService
from schemas.sgr_schema import SGRSchema, SGRResponse

router = APIRouter()
service = SGRService()

@router.post("/sgr", response_model=SGRResponse)
def create_sgr(sgr: SGRSchema):
    return service.create_sgr(sgr)

@router.get("/sgr", response_model=List[SGRResponse])
def get_sgrs():
    return service.get_sgrs()

@router.get("/sgr/{sgr_id}", response_model=SGRResponse)
def get_sgr_by_id(sgr_id: int):
    sgr = service.get_sgr_by_id(sgr_id)
    if sgr is None:
        raise HTTPException(status_code=404, detail="SGR not found")
    return sgr

@router.put("/sgr/{sgr_id}", response_model=SGRResponse)
def update_sgr(sgr_id: int, sgr: SGRSchema):
    return service.update_sgr(sgr_id, sgr)

@router.delete("/sgr/{sgr_id}", response_model=bool)
def delete_sgr(sgr_id: int):
    success = service.delete_sgr(sgr_id)
    if not success:
        raise HTTPException(status_code=404, detail="SGR not found")
    return success