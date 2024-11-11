from repositories.project_repository import ProjectRepository
from schemas.project_schema import ProjectCreate, ProjectResponse
import logging

class ProjectService:
    def __init__(self):
        self.repo = ProjectRepository()

    def create_project(self, project: ProjectCreate) -> ProjectResponse:
        if not project.description:
            raise ValueError("Description cannot be empty")

        project.description = project.description.strip()

        response = self.repo.create_project(project)

        logging.info(f"Project created with ID: {response.id}")

        return response

    def get_projects(self):
        projects = self.repo.get_projects()

        return projects

    def get_project_by_id(self, project_id: int):
        if project_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_project_by_id(project_id)

    def update_project(self, project_id: int, project: ProjectCreate) -> ProjectResponse:
        if not project.description:
            raise ValueError("Description cannot be empty")

        project.description = project.description.strip()

        response = self.repo.update_project(project_id, project)

        logging.info(f"Project with ID: {project_id} updated")

        return response

    def delete_project(self, project_id: int) -> bool:
        if project_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_project(project_id)

        if success:
            logging.info(f"Project with ID: {project_id} deleted")
        else:
            logging.warning(f"Project with ID: {project_id} not found")

        return success