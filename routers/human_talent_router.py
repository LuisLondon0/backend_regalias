from fastapi import APIRouter, HTTPException
from typing import List
from services.human_talent_service import HumanTalentService
from schemas.human_talent_schema import HumanTalentCreate, HumanTalentResponse

router = APIRouter()
service = HumanTalentService()

@router.post("/human_talents", response_model=HumanTalentResponse)
def create_human_talent(human_talent: HumanTalentCreate):
    return service.create_human_talent(human_talent)

@router.get("/human_talents", response_model=List[HumanTalentResponse])
def get_human_talents():
    return service.get_human_talents()

@router.get("/human_talents/{human_talent_id}", response_model=HumanTalentResponse)
def get_human_talent_by_id(human_talent_id: int):
    human_talent = service.get_human_talent_by_id(human_talent_id)
    if human_talent is None:
        raise HTTPException(status_code=404, detail="Human talent not found")
    return human_talent

@router.put("/human_talents/{human_talent_id}", response_model=HumanTalentResponse)
def update_human_talent(human_talent_id: int, human_talent: HumanTalentCreate):
    return service.update_human_talent(human_talent_id, human_talent)

@router.delete("/human_talents/{human_talent_id}", response_model=bool)
def delete_human_talent(human_talent_id: int):
    success = service.delete_human_talent(human_talent_id)
    if not success:
        raise HTTPException(status_code=404, detail="Human talent not found")
    return success

@router.post("/human_talents/budget/{project_id}", response_model=bool)
def create_budget(project_id: int):
    return service.create_budget(project_id)

@router.get("/human_talents/budget_per_talent/{project_id}")
def get_budget_per_talent(project_id: int):
    return service.get_budget_per_talent(project_id)

@router.get("/human_talents/total_budget_per_talent/{project_id}")
def get_total_budget_per_talent(project_id: int):
    return service.get_total_budget_per_talent(project_id)