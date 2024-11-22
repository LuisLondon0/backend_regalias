from database import DatabaseConnection
from schemas.users_projects_schema import UserProjectCreate, UserProjectResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class UsersProjectsRepository:
    def create_user_project(self, user_project: UserProjectCreate) -> UserProjectResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO userprojects (userid, projectid) VALUES (%s, %s) RETURNING userprojectid", 
                        (user_project.user_id, user_project.project_id)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return UserProjectResponse(id=id, user_id=user_project.user_id, project_id=user_project.project_id)
        except Exception as e:
            logging.error(f"Error creating user-project relationship: {e}")
            raise

    def get_user_projects(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM userprojects")
                    user_projects = cursor.fetchall()
                    if user_projects:
                        return [
                            UserProjectResponse(id=user_project[0], user_id=user_project[1], project_id=user_project[2]) 
                            for user_project in user_projects
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching user-project relationships: {e}")
            raise

    def get_user_project_by_id(self, id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM userprojects WHERE userprojectid = %s", (id,))
                    user_project = cursor.fetchone()
                    if user_project:
                        return UserProjectResponse(id=user_project[0], user_id=user_project[1], project_id=user_project[2])
                    return None
        except Exception as e:
            logging.error(f"Error fetching user-project relationship by id {id}: {e}")
            raise

    def get_user_projects_by_user_id(self, user_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM userprojects WHERE userid = %s", (user_id,))
                    user_projects = cursor.fetchall()
                    if user_projects:
                        return [
                            UserProjectResponse(id=user_project[0], user_id=user_project[1], project_id=user_project[2]) 
                            for user_project in user_projects
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching user-project relationships by user_id {user_id}: {e}")
            raise

    def get_user_projects_by_project_id(self, project_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM userprojects WHERE projectid = %s", (project_id,))
                    user_projects = cursor.fetchall()
                    if user_projects:
                        return [
                            UserProjectResponse(id=user_project[0], user_id=user_project[1], project_id=user_project[2]) 
                            for user_project in user_projects
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching user-project relationships by project_id {project_id}: {e}")
            raise

    def update_user_project(self, id: int, user_project: UserProjectCreate) -> UserProjectResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE userprojects SET userid = %s, projectid = %s WHERE userprojectid = %s", 
                        (user_project.user_id, user_project.project_id, id)
                    )
                    conn.commit()
                    return UserProjectResponse(id=id, user_id=user_project.user_id, project_id=user_project.project_id)
        except Exception as e:
            logging.error(f"Error updating user-project relationship: {e}")
            raise

    def delete_user_project(self, id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM userprojects WHERE userprojectid = %s", (id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No user-project relationship found with id {id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting user-project relationship: {e}")
            raise

    def check_user_project_exists(self, user_id: int, project_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM userprojects WHERE userid = %s AND projectid = %s",
                        (user_id, project_id)
                    )
                    return cursor.fetchone() is not None
        except Exception as e:
            logging.error(f"Error checking if user-project relationship exists: {e}")
            raise