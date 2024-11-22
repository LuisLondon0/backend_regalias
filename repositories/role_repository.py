from database import DatabaseConnection
from schemas.role_schema import RoleCreate, RoleResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class RoleRepository:
    def create_role(self, role: RoleCreate) -> RoleResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO roles (description) VALUES (%s) RETURNING roleid", 
                        (role.description,)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return RoleResponse(id=id, description=role.description)
        except Exception as e:
            logging.error(f"Error creating role: {e}")
            raise

    def get_roles(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM roles")
                    roles = cursor.fetchall()
                    if roles:
                        return [
                            RoleResponse(id=role[0], description=role[1]) 
                            for role in roles
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching roles: {e}")
            raise

    def get_role_by_id(self, role_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM roles WHERE roleid = %s", (role_id,))
                    role = cursor.fetchone()
                    if role:
                        return RoleResponse(id=role[0], description=role[1])
                    return None
        except Exception as e:
            logging.error(f"Error fetching role by id {role_id}: {e}")
            raise

    def get_role_by_description(self, description: str):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM roles WHERE description = %s", (description,))
                    role = cursor.fetchone()
                    if role:
                        return RoleResponse(id=role[0], description=role[1])
                    return None
        except Exception as e:
            logging.error(f"Error fetching role by description {description}: {e}")
            raise

    def update_role(self, role_id: int, role: RoleCreate) -> RoleResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE roles SET description = %s WHERE roleid = %s", 
                        (role.description, role_id)
                    )
                    conn.commit()
                    return RoleResponse(id=role_id, description=role.description)
        except Exception as e:
            logging.error(f"Error updating role: {e}")
            raise

    def delete_role(self, role_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM roles WHERE roleid = %s", (role_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No role found with id {role_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting role: {e}")
            raise