from repositories.week_repository import WeekRepository
from schemas.week_schema import WeekCreate, WeekResponse
import logging

class WeekService:
    def __init__(self):
        self.repo = WeekRepository()

    def create_week(self, week: WeekCreate) -> WeekResponse:
        if week.week <= 0:
            raise ValueError("Week number must be a positive integer")

        response = self.repo.create_week(week)

        logging.info(f"Week created with ID: {response.id}")

        return response

    def get_weeks(self):
        weeks = self.repo.get_weeks()

        return weeks

    def get_week_by_id(self, week_id: int):
        if week_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_week_by_id(week_id)

    def update_week(self, week_id: int, week: WeekCreate) -> WeekResponse:
        if week.week <= 0:
            raise ValueError("Week number must be a positive integer")

        response = self.repo.update_week(week_id, week)

        logging.info(f"Week with ID: {week_id} updated")

        return response

    def delete_week(self, week_id: int) -> bool:
        if week_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_week(week_id)

        if success:
            logging.info(f"Week with ID: {week_id} deleted")
        else:
            logging.warning(f"Week with ID: {week_id} not found")

        return success