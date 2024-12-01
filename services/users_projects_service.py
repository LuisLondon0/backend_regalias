from repositories.users_projects_repository import UsersProjectsRepository
from schemas.users_projects_schema import UserProjectCreate
from services.user_service import UserService
from services.project_service import ProjectService
import logging

class UsersProjectsService:
    def __init__(self):
        self.repo = UsersProjectsRepository()
        self.user_service = UserService()
        self.project_service = ProjectService()

    def create_user_project(self, user_project: UserProjectCreate) -> UserProjectCreate:
        user = self.user_service.get_user_by_id(user_project.user_id)
        if not user:
            raise ValueError("User does not exist")

        project = self.project_service.get_project_by_id(user_project.project_id)
        if not project:
            raise ValueError("Project does not exist")

        if self.repo.check_user_project_exists(user_project.user_id, user_project.project_id):
            raise ValueError("This user is already associated with the specified project")

        response = self.repo.create_user_project(user_project)
        logging.info(f"User-Project relationship created with ID: {response.id}")

        return response

    def get_user_projects(self):
        user_projects = self.repo.get_user_projects()
        return user_projects

    def get_user_project_by_id(self, id: int) -> UserProjectCreate:
        if id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_user_project_by_id(id)
    
    def get_user_projects_by_user_id(self, user_id: int):
        if user_id <= 0:
            raise ValueError("ID must be a positive integer")
        return self.repo.get_user_projects_by_user_id(user_id)

    def get_user_projects_by_project_id(self, project_id: int):
        if project_id <= 0:
            raise ValueError("ID must be a positive integer")
        return self.repo.get_user_projects_by_project_id(project_id)

    def update_user_project(self, id: int, user_project: UserProjectCreate) -> UserProjectCreate:
        user = self.user_service.get_user_by_id(user_project.user_id)
        if not user:
            raise ValueError("User does not exist")

        project = self.project_service.get_project_by_id(user_project.project_id)
        if not project:
            raise ValueError("Project does not exist")

        if self.repo.check_user_project_exists(user_project.user_id, user_project.project_id):
            raise ValueError("This user is already associated with the specified project")

        response = self.repo.update_user_project(id, user_project)
        logging.info(f"User-Project relationship with ID: {id} updated")

        return response

    def delete_user_project(self, id: int) -> bool:
        if id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_user_project(id)

        if success:
            logging.info(f"User-Project relationship with ID: {id} deleted")
        else:
            logging.warning(f"User-Project relationship with ID: {id} not found")

        return success