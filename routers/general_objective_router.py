from fastapi import APIRouter, HTTPException
from typing import List
from services.general_objective_service import GeneralObjectiveService
from schemas.general_objective_schema import GeneralObjectiveCreate, GeneralObjectiveResponse

router = APIRouter()
service = GeneralObjectiveService()

@router.post("/general_objectives", response_model=GeneralObjectiveResponse)
def create_general_objective(general_objective: GeneralObjectiveCreate):
    try:
        return service.create_general_objective(general_objective)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/general_objectives", response_model=List[GeneralObjectiveResponse])
def get_general_objectives():
    try:
        return service.get_general_objectives()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/general_objectives/{general_objective_id}", response_model=GeneralObjectiveResponse)
def get_general_objective_by_id(general_objective_id: int):
    try:
        objective = service.get_general_objective_by_id(general_objective_id)
        if objective is None:
            raise HTTPException(status_code=404, detail="General Objective not found")
        return objective
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/general_objectives/{general_objective_id}", response_model=GeneralObjectiveResponse)
def update_general_objective(general_objective_id: int, general_objective: GeneralObjectiveCreate):
    try:
        return service.update_general_objective(general_objective_id, general_objective)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/general_objectives/{general_objective_id}", response_model=bool)
def delete_general_objective(general_objective_id: int):
    try:
        success = service.delete_general_objective(general_objective_id)
        if not success:
            raise HTTPException(status_code=404, detail="General Objective not found")
        return success
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    

@router.get("/test/{id}", response_model=str)
def get_test(id: int):
    try:
        objective = "Prueba exitosa {id}".format(id=id)
        return objective
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")
