from fastapi import APIRouter, HTTPException, Depends
from typing import List
from services.users_projects_service import UsersProjectsService
from schemas.users_projects_schema import UserProjectCreate, UserProjectResponse
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
service = UsersProjectsService()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/users-projects", response_model=UserProjectResponse)
def create_user_project(user_project: UserProjectCreate):
    return service.create_user_project(user_project)

@router.get("/users-projects", response_model=List[UserProjectResponse])
def get_user_projects():
    return service.get_user_projects()

@router.get("/users-projects/{id}", response_model=UserProjectResponse)
def get_user_project_by_id(id: int):
    user_project = service.get_user_project_by_id(id)
    if user_project is None:
        raise HTTPException(status_code=404, detail="User-Project relationship not found")
    return user_project

@router.get("/users-projects/user/{user_id}", response_model=List[UserProjectResponse])
def get_user_projects_by_user_id(user_id: int):
    user_projects = service.get_user_projects_by_user_id(user_id)
    if not user_projects:
        raise HTTPException(status_code=404, detail="User-Project relationships not found for user_id")
    return user_projects

@router.get("/users-projects/project/{project_id}", response_model=List[UserProjectResponse])
def get_user_projects_by_project_id(project_id: int):
    user_projects = service.get_user_projects_by_project_id(project_id)
    if not user_projects:
        raise HTTPException(status_code=404, detail="User-Project relationships not found for project_id")
    return user_projects

@router.put("/users-projects/{id}", response_model=UserProjectResponse)
def update_user_project(id: int, user_project: UserProjectCreate):
    return service.update_user_project(id, user_project)

@router.delete("/users-projects/{id}", response_model=bool)
def delete_user_project(id: int):
    success = service.delete_user_project(id)
    if not success:
        raise HTTPException(status_code=404, detail="User-Project relationship not found")
    return success