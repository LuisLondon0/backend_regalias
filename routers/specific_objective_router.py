from fastapi import APIRouter, HTTPException
from typing import List
from services.specific_objective_service import SpecificObjectiveService
from schemas.specific_objective_schema import SpecificObjectiveCreate, SpecificObjectiveResponse

router = APIRouter()
service = SpecificObjectiveService()

@router.post("/specific_objectives", response_model=SpecificObjectiveResponse)
def create_specific_objective(specific_objective: SpecificObjectiveCreate):
    try:
        return service.create_specific_objective(specific_objective)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/specific_objectives", response_model=List[SpecificObjectiveResponse])
def get_specific_objectives():
    try:
        return service.get_specific_objectives()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/specific_objectives/{specific_objective_id}", response_model=SpecificObjectiveResponse)
def get_specific_objective_by_id(specific_objective_id: int):
    try:
        objective = service.get_specific_objective_by_id(specific_objective_id)
        if objective is None:
            raise HTTPException(status_code=404, detail="Specific Objective not found")
        return objective
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/specific_objectives/{specific_objective_id}", response_model=SpecificObjectiveResponse)
def update_specific_objective(specific_objective_id: int, specific_objective: SpecificObjectiveCreate):
    try:
        return service.update_specific_objective(specific_objective_id, specific_objective)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/specific_objectives/{specific_objective_id}", response_model=bool)
def delete_specific_objective(specific_objective_id: int):
    try:
        success = service.delete_specific_objective(specific_objective_id)
        if not success:
            raise HTTPException(status_code=404, detail="Specific Objective not found")
        return success
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")