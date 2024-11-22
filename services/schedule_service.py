from repositories.schedule_repository import ScheduleRepository
from repositories.task_repository import TaskRepository
from repositories.month_repository import MonthRepository
from schemas.schedule_schema import ScheduleCreate, ScheduleResponse
import logging

class ScheduleService:
    def __init__(self):
        self.schedule_repo = ScheduleRepository()
        self.task_repo = TaskRepository()
        self.month_repo = MonthRepository()

    def create_schedule(self, schedule: ScheduleCreate) -> ScheduleResponse:
        task = self.task_repo.get_task_by_id(schedule.task_id)
        if not task:
            raise ValueError("Task does not exist")

        month = self.month_repo.get_month_by_id(schedule.month_id)
        if not month:
            raise ValueError("Month does not exist")

        if self.schedule_repo.check_schedule_exists(schedule.task_id, schedule.month_id):
            raise ValueError("This task is already scheduled for the specified month")

        response = self.schedule_repo.create_schedule(schedule)
        logging.info(f"Schedule created with ID: {response.id}")
        
        return response

    def get_schedules(self):
        schedules = self.schedule_repo.get_schedules()
        return schedules

    def get_schedule_by_id(self, schedule_id: int):
        if schedule_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.schedule_repo.get_schedule_by_id(schedule_id)

    def get_schedules_by_month_id(self, month_id: int):
        if month_id <= 0:
            raise ValueError("ID must be a positive integer")
        return self.schedule_repo.get_schedules_by_month_id(month_id)

    def get_schedules_by_task_id(self, task_id: int):
        if task_id <= 0:
            raise ValueError("ID must be a positive integer")
        return self.schedule_repo.get_schedules_by_task_id(task_id)

    def update_schedule(self, schedule_id: int, schedule: ScheduleCreate) -> ScheduleResponse:
        task = self.task_repo.get_task_by_id(schedule.task_id)
        if not task:
            raise ValueError("Task does not exist")

        month = self.month_repo.get_month_by_id(schedule.month_id)
        if not month:
            raise ValueError("Month does not exist")

        if self.schedule_repo.check_schedule_exists(schedule.task_id, schedule.month_id):
            raise ValueError("This task is already scheduled for the specified month")

        response = self.schedule_repo.update_schedule(schedule_id, schedule)
        logging.info(f"Schedule with ID: {schedule_id} updated")

        return response

    def delete_schedule(self, schedule_id: int) -> bool:
        if schedule_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.schedule_repo.delete_schedule(schedule_id)

        if success:
            logging.info(f"Schedule with ID: {schedule_id} deleted")
        else:
            logging.warning(f"Schedule with ID: {schedule_id} not found")

        return success