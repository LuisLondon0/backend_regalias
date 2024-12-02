from repositories.sgr_repository import SGRRepository
from schemas.sgr_schema import SGRSchema, SGRResponse
import logging

class SGRService:
    def __init__(self):
        self.repo = SGRRepository()

    def create_sgr(self, sgr: SGRSchema) -> SGRResponse:
        if not sgr.resourcetype:
            raise ValueError("Resource type cannot be empty")
        if sgr.cash < 0:
            raise ValueError("Cash value cannot be negative")

        sgr.resourcetype = sgr.resourcetype.strip()

        response = self.repo.create_sgr(sgr)

        logging.info(f"SGR created with ID: {response.id}")

        return response

    def get_sgrs(self):
        return self.repo.get_sgrs()

    def get_sgr_by_id(self, sgr_id: int):
        if sgr_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_sgr_by_id(sgr_id)

    def update_sgr(self, sgr_id: int, sgr: SGRSchema) -> SGRResponse:
        if not sgr.resourcetype:
            raise ValueError("Resource type cannot be empty")
        if sgr.cash < 0:
            raise ValueError("Cash value cannot be negative")

        sgr.resourcetype = sgr.resourcetype.strip()

        response = self.repo.update_sgr(sgr_id, sgr)

        logging.info(f"SGR with ID: {sgr_id} updated")

        return response

    def delete_sgr(self, sgr_id: int) -> bool:
        if sgr_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_sgr(sgr_id)

        if success:
            logging.info(f"SGR with ID: {sgr_id} deleted")
        else:
            logging.warning(f"SGR with ID: {sgr_id} not found")

        return success