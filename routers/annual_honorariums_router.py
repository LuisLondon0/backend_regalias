from fastapi import APIRouter, HTTPException
from typing import List
from services.annual_honorariums_service import AnnualHonorariumsService
from schemas.annual_honorariums_schema import AnnualHonorariumsSchema, AnnualHonorariumsResponse

router = APIRouter()
service = AnnualHonorariumsService()

@router.post("/annual_honorariums", response_model=AnnualHonorariumsResponse)
def create_annual_honorarium(honorarium: AnnualHonorariumsSchema):
    return service.create_annual_honorarium(honorarium)

@router.get("/annual_honorariums", response_model=List[AnnualHonorariumsResponse])
def get_annual_honorariums():
    return service.get_annual_honorariums()

@router.get("/annual_honorariums/{honorarium_id}", response_model=AnnualHonorariumsResponse)
def get_annual_honorarium_by_id(honorarium_id: int):
    honorarium = service.get_annual_honorarium_by_id(honorarium_id)
    if honorarium is None:
        raise HTTPException(status_code=404, detail="Annual honorarium not found")
    return honorarium

@router.put("/annual_honorariums/{honorarium_id}", response_model=AnnualHonorariumsResponse)
def update_annual_honorarium(honorarium_id: int, honorarium: AnnualHonorariumsSchema):
    return service.update_annual_honorarium(honorarium_id, honorarium)

@router.delete("/annual_honorariums/{honorarium_id}", response_model=bool)
def delete_annual_honorarium(honorarium_id: int):
    success = service.delete_annual_honorarium(honorarium_id)
    if not success:
        raise HTTPException(status_code=404, detail="Annual honorarium not found")
    return success