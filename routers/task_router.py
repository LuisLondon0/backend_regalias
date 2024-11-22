from fastapi import APIRouter, HTTPException
from typing import List
from services.task_service import TaskService
from schemas.task_schema import TaskCreate, TaskResponse

router = APIRouter()
service = TaskService()

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    return service.create_task(task)

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    return service.get_tasks()

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int):
    task = service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate):
    return service.update_task(task_id, task)

@router.delete("/tasks/{task_id}", response_model=bool)
def delete_task(task_id: int):
    success = service.delete_task(task_id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return success