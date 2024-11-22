from repositories.specific_objective_repository import SpecificObjectiveRepository
from schemas.specific_objective_schema import SpecificObjectiveCreate, SpecificObjectiveResponse
from services.project_service import ProjectService
import logging

class SpecificObjectiveService:
    def __init__(self):
        self.repo = SpecificObjectiveRepository()
        self.project_service = ProjectService()

    def create_specific_objective(self, specific_objective: SpecificObjectiveCreate) -> SpecificObjectiveResponse:
        project = self.project_service.get_project_by_id(specific_objective.project_id)
        if not project:
            raise ValueError("Project does not exist")

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
        project = self.project_service.get_project_by_id(specific_objective.project_id)
        if not project:
            raise ValueError("Project does not exist")

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