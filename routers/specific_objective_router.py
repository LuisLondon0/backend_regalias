from fastapi import APIRouter, HTTPException
from typing import List
from services.specific_objective_service import SpecificObjectiveService
from schemas.specific_objective_schema import SpecificObjectiveCreate, SpecificObjectiveResponse

router = APIRouter()
service = SpecificObjectiveService()

@router.post("/specific_objectives", response_model=SpecificObjectiveResponse)
def create_specific_objective(specific_objective: SpecificObjectiveCreate):
    return service.create_specific_objective(specific_objective)

@router.get("/specific_objectives", response_model=List[SpecificObjectiveResponse])
def get_specific_objectives():
    return service.get_specific_objectives()

@router.get("/specific_objectives/{specific_objective_id}", response_model=SpecificObjectiveResponse)
def get_specific_objective_by_id(specific_objective_id: int):
    objective = service.get_specific_objective_by_id(specific_objective_id)
    if objective is None:
        raise HTTPException(status_code=404, detail="Specific Objective not found")
    return objective

@router.put("/specific_objectives/{specific_objective_id}", response_model=SpecificObjectiveResponse)
def update_specific_objective(specific_objective_id: int, specific_objective: SpecificObjectiveCreate):
    return service.update_specific_objective(specific_objective_id, specific_objective)

@router.delete("/specific_objectives/{specific_objective_id}", response_model=bool)
def delete_specific_objective(specific_objective_id: int):
    success = service.delete_specific_objective(specific_objective_id)
    if not success:
        raise HTTPException(status_code=404, detail="Specific Objective not found")
    return success