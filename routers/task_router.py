from fastapi import APIRouter, HTTPException
from typing import List
from services.task_service import TaskService
from schemas.task_schema import TaskCreate, TaskResponse

router = APIRouter()
service = TaskService()

@router.post("/tasks", response_model=TaskResponse)
def create_task(task: TaskCreate):
    try:
        return service.create_task(task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/tasks", response_model=List[TaskResponse])
def get_tasks():
    try:
        return service.get_tasks()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int):
    try:
        task = service.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail="Task not found")
        return task
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, task: TaskCreate):
    try:
        return service.update_task(task_id, task)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")

@router.delete("/tasks/{task_id}", response_model=bool)
def delete_task(task_id: int):
    try:
        success = service.delete_task(task_id)
        if not success:
            raise HTTPException(status_code=404, detail="Task not found")
        return success
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal Server Error")