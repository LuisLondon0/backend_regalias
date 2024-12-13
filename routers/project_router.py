from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import List
from services.project_service import ProjectService
from schemas.project_schema import ProjectCreate, ProjectResponse
from schemas.summary_schema import Summary, SummaryResponse
router = APIRouter()
service = ProjectService()

@router.post("/projects", response_model=ProjectResponse)
def create_project(project: ProjectCreate):
    return service.create_project(project)

@router.post("/projects/from-excel", response_model=List[ProjectResponse])
async def create_projects_from_excel(file: UploadFile = File(...)):
    return await service.create_projects_from_excel(file)

@router.get("/projects", response_model=List[ProjectResponse])
def get_projects():
    return service.get_projects()

@router.get("/projects/{project_id}", response_model=ProjectResponse)
def get_project_by_id(project_id: int):
    project = service.get_project_by_id(project_id)
    if project is None:
        raise HTTPException(status_code=404, detail="Project not found")
    return project

@router.put("/projects/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project: ProjectCreate):
    return service.update_project(project_id, project)

@router.delete("/projects/{project_id}", response_model=bool)
def delete_project(project_id: int):
    success = service.delete_project(project_id)
    if not success:
        raise HTTPException(status_code=404, detail="Project not found")
    return success

@router.get("/summary", response_model=SummaryResponse)
def get_summary():
    summary = service.get_summary()
    if summary is None:
        raise HTTPException(status_code=404, detail="Summary not found")
    return summary