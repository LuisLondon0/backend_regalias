from repositories.general_objective_repository import GeneralObjectiveRepository
from schemas.general_objective_schema import GeneralObjectiveCreate, GeneralObjectiveResponse
import logging

class GeneralObjectiveService:
    def __init__(self):
        self.repo = GeneralObjectiveRepository()

    def create_general_objective(self, general_objective: GeneralObjectiveCreate) -> GeneralObjectiveResponse:
        if not general_objective.description:
            raise ValueError("Description cannot be empty")

        general_objective.description = general_objective.description.strip()

        response = self.repo.create_general_objective(general_objective)

        logging.info(f"General objective created with ID: {response.id}")

        return response

    def get_general_objectives(self):
        objectives = self.repo.get_general_objectives()

        return objectives

    def get_general_objective_by_id(self, general_objective_id: int):
        if general_objective_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_general_objective_by_id(general_objective_id)

    def update_general_objective(self, general_objective_id: int, general_objective: GeneralObjectiveCreate) -> GeneralObjectiveResponse:
        if not general_objective.description:
            raise ValueError("Description cannot be empty")

        general_objective.description = general_objective.description.strip()

        response = self.repo.update_general_objective(general_objective_id, general_objective)

        logging.info(f"General objective with ID: {general_objective_id} updated")

        return response

    def delete_general_objective(self, general_objective_id: int) -> bool:
        if general_objective_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_general_objective(general_objective_id)

        if success:
            logging.info(f"General objective with ID: {general_objective_id} deleted")
        else:
            logging.warning(f"General objective with ID: {general_objective_id} not found")

        return success