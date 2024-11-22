from repositories.month_repository import MonthRepository
from schemas.month_schema import MonthCreate, MonthResponse
import logging

class MonthService:
    def __init__(self):
        self.repo = MonthRepository()

    def create_month(self, month: MonthCreate) -> MonthResponse:
        if not month.month:
            raise ValueError("Month name cannot be empty")

        response = self.repo.create_month(month)

        logging.info(f"Month created with ID: {response.id}")

        return response

    def get_months(self):
        months = self.repo.get_months()
        return months

    def get_month_by_id(self, month_id: int):
        if month_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_month_by_id(month_id)

    def update_month(self, month_id: int, month: MonthCreate) -> MonthResponse:
        if not month.month:
            raise ValueError("Month name cannot be empty")

        response = self.repo.update_month(month_id, month)

        logging.info(f"Month with ID: {month_id} updated")

        return response

    def delete_month(self, month_id: int) -> bool:
        if month_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_month(month_id)

        if success:
            logging.info(f"Month with ID: {month_id} deleted")
        else:
            logging.warning(f"Month with ID: {month_id} not found")

        return success