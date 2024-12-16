from repositories.task_repository import TaskRepository
from schemas.activity_schema import ActivityCreate, ActivityResponse
from services.activity_service import ActivityService
import logging

class TaskService:
    def __init__(self):
        self.repo = TaskRepository()
        self.activity_service = ActivityService()

    def create_task(self, task: ActivityCreate) -> ActivityResponse:
        activity = self.activity_service.get_activity_by_id(task.activity_id)
        if not activity:
            raise ValueError("Activity does not exist")

        if not task.description:
            raise ValueError("Description cannot be empty")

        task.description = task.description.strip()

        response = self.repo.create_task(task)

        logging.info(f"Task created with ID: {response.id}")

        return response

    def get_tasks(self):
        tasks = self.repo.get_tasks()
        return tasks
    
    def get_task_by_id(self, task_id: int):
        if task_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_task_by_id(task_id)

    def update_task(self, task_id: int, task: ActivityCreate) -> ActivityResponse:
        activity = self.activity_service.get_activity_by_id(task.activity_id)
        if not activity:
            raise ValueError("Activity does not exist")

        if not task.description:
            raise ValueError("Description cannot be empty")

        task.description = task.description.strip()

        response = self.repo.update_task(task_id, task)

        logging.info(f"Task with ID: {task_id} updated")

        return response

    def delete_task(self, task_id: int) -> bool:
        if task_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_task(task_id)

        if success:
            logging.info(f"Task with ID: {task_id} deleted")
        else:
            logging.warning(f"Task with ID: {task_id} not found")

        return success
    
    def get_tasks_by_activity(self, activity_id: int):
        tasks = self.repo.get_tasks_by_activity(activity_id)
        return tasks