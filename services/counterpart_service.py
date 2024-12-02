from repositories.counterpart_repository import CounterpartRepository
from schemas.counterpart_schema import CounterpartSchema, CounterpartResponse
import logging

class CounterpartService:
    def __init__(self):
        self.repo = CounterpartRepository()

    def create_counterpart(self, counterpart: CounterpartSchema) -> CounterpartResponse:
        if not counterpart.resorucetype:
            raise ValueError("Resource type cannot be empty")
        if not counterpart.entity:
            raise ValueError("Entity cannot be empty")
        if counterpart.inkind < 0:
            raise ValueError("In-kind value cannot be negative")
        if counterpart.cash < 0:
            raise ValueError("Cash value cannot be negative")

        counterpart.resorucetype = counterpart.resorucetype.strip()
        counterpart.entity = counterpart.entity.strip()

        response = self.repo.create_counterpart(counterpart)

        logging.info(f"Counterpart created with ID: {response.id}")

        return response

    def get_counterparts(self):
        return self.repo.get_counterparts()

    def get_counterpart_by_id(self, counterpart_id: int):
        if counterpart_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_counterpart_by_id(counterpart_id)

    def update_counterpart(self, counterpart_id: int, counterpart: CounterpartSchema) -> CounterpartResponse:
        if not counterpart.resorucetype:
            raise ValueError("Resource type cannot be empty")
        if not counterpart.entity:
            raise ValueError("Entity cannot be empty")
        if counterpart.inkind < 0:
            raise ValueError("In-kind value cannot be negative")
        if counterpart.cash < 0:
            raise ValueError("Cash value cannot be negative")

        counterpart.resorucetype = counterpart.resorucetype.strip()
        counterpart.entity = counterpart.entity.strip()

        response = self.repo.update_counterpart(counterpart_id, counterpart)

        logging.info(f"Counterpart with ID: {counterpart_id} updated")

        return response

    def delete_counterpart(self, counterpart_id: int) -> bool:
        if counterpart_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_counterpart(counterpart_id)

        if success:
            logging.info(f"Counterpart with ID: {counterpart_id} deleted")
        else:
            logging.warning(f"Counterpart with ID: {counterpart_id} not found")

        return success