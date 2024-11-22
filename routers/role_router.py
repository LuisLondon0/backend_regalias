from fastapi import APIRouter, HTTPException
from typing import List
from services.role_service import RoleService
from schemas.role_schema import RoleCreate, RoleResponse

router = APIRouter()
service = RoleService()

@router.post("/roles", response_model=RoleResponse)
def create_role(role: RoleCreate):
    return service.create_role(role)

@router.get("/roles", response_model=List[RoleResponse])
def get_roles():
    return service.get_roles()

@router.get("/roles/{role_id}", response_model=RoleResponse)
def get_role_by_id(role_id: int):
    role = service.get_role_by_id(role_id)
    if role is None:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleCreate):
    return service.update_role(role_id, role)

@router.delete("/roles/{role_id}", response_model=bool)
def delete_role(role_id: int):
    success = service.delete_role(role_id)
    if not success:
        raise HTTPException(status_code=404, detail="Role not found")
    return success