from fastapi import APIRouter, HTTPException
from typing import List
from services.project_service import ProjectService
from schemas.project_schema import ProjectCreate, ProjectResponse

router = APIRouter()
service = ProjectService()

@router.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate):
    try:
        return service.create_project(project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects():
    try:
        return service.get_projects()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project_by_id(project_id: int):
    try:
        project = service.get_project_by_id(project_id)
        if project is None:
            raise HTTPException(status_code=404, detail="Project not found")
        return project
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectCreate):
    try:
        return service.update_project(project_id, project)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/projects/{project_id}", response_model=bool)
def delete_project(project_id: int):
    try:
        success = service.delete_project(project_id)
        if not success:
            raise HTTPException(status_code=404, detail="Project not found")
        return success
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")