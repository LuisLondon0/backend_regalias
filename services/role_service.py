from repositories.role_repository import RoleRepository
from schemas.role_schema import RoleCreate, RoleResponse
import logging
from fastapi import HTTPException

class RoleService:
    def __init__(self):
        self.repo = RoleRepository()

    def create_role(self, role: RoleCreate) -> RoleResponse:
        if not role.description:
            raise ValueError("Description cannot be empty")

        role.description = role.description.strip().upper()
        existing_role = self.repo.get_role_by_description(role.description)
        if existing_role:
            raise HTTPException(status_code=409, detail="Role already exists")

        response = self.repo.create_role(role)

        logging.info(f"Role created with ID: {response.id}")

        return response

    def get_roles(self):
        roles = self.repo.get_roles()

        return roles

    def get_role_by_id(self, role_id: int):
        if role_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_role_by_id(role_id)

    def update_role(self, role_id: int, role: RoleCreate) -> RoleResponse:
        if not role.description:
            raise ValueError("Description cannot be empty")

        role.description = role.description.strip().upper()

        response = self.repo.update_role(role_id, role)

        logging.info(f"Role with ID: {role_id} updated")

        return response

    def delete_role(self, role_id: int) -> bool:
        if role_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_role(role_id)

        if success:
            logging.info(f"Role with ID: {role_id} deleted")
        else:
            logging.warning(f"Role with ID: {role_id} not found")

        return success