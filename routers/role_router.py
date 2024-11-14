from fastapi import APIRouter, HTTPException
from typing import List
from services.role_service import RoleService
from schemas.role_schema import RoleCreate, RoleResponse

router = APIRouter()
service = RoleService()

@router.post("/roles", response_model=RoleResponse)
def create_role(role: RoleCreate):
    try:
        return service.create_role(role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/roles", response_model=List[RoleResponse])
def get_roles():
    try:
        return service.get_roles()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/roles/{role_id}", response_model=RoleResponse)
def get_role_by_id(role_id: int):
    try:
        role = service.get_role_by_id(role_id)
        if role is None:
            raise HTTPException(status_code=404, detail="Role not found")
        return role
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/roles/{role_id}", response_model=RoleResponse)
def update_role(role_id: int, role: RoleCreate):
    try:
        return service.update_role(role_id, role)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/roles/{role_id}", response_model=bool)
def delete_role(role_id: int):
    try:
        success = service.delete_role(role_id)
        if not success:
            raise HTTPException(status_code=404, detail="Role not found")
        return success
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")