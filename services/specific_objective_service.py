from repositories.specific_objective_repository import SpecificObjectiveRepository
from schemas.specific_objective_schema import SpecificObjectiveCreate, SpecificObjectiveResponse
from services.general_objective_service import GeneralObjectiveService
import logging

class SpecificObjectiveService:
    def __init__(self):
        self.repo = SpecificObjectiveRepository()
        self.general_objective_service = GeneralObjectiveService()

    def create_specific_objective(self, specific_objective: SpecificObjectiveCreate) -> SpecificObjectiveResponse:
        general_objective = self.general_objective_service.get_general_objective_by_id(specific_objective.general_objective_id)
        if not general_objective:
            raise ValueError("General objective does not exist")

        if not specific_objective.description:
            raise ValueError("Description cannot be empty")

        specific_objective.description = specific_objective.description.strip()

        response = self.repo.create_specific_objective(specific_objective)

        logging.info(f"Specific objective created with ID: {response.id}")

        return response

    def get_specific_objectives(self):
        objectives = self.repo.get_specific_objectives()
        return objectives

    def get_specific_objective_by_id(self, specific_objective_id: int):
        if specific_objective_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_specific_objective_by_id(specific_objective_id)

    def update_specific_objective(self, specific_objective_id: int, specific_objective: SpecificObjectiveCreate) -> SpecificObjectiveResponse:
        general_objective = self.general_objective_service.get_general_objective_by_id(specific_objective.general_objective_id)
        if not general_objective:
            raise ValueError("General objective does not exist")

        if not specific_objective.description:
            raise ValueError("Description cannot be empty")

        specific_objective.description = specific_objective.description.strip()

        response = self.repo.update_specific_objective(specific_objective_id, specific_objective)

        logging.info(f"Specific objective with ID: {specific_objective_id} updated")

        return response

    def delete_specific_objective(self, specific_objective_id: int) -> bool:
        if specific_objective_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_specific_objective(specific_objective_id)

        if success:
            logging.info(f"Specific objective with ID: {specific_objective_id} deleted")
        else:
            logging.warning(f"Specific objective with ID: {specific_objective_id} not found")

        return success