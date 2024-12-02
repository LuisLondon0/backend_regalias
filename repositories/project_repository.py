from database.database import DatabaseConnection
from schemas.project_schema import ProjectCreate, ProjectResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ProjectRepository:
    def create_project(self, project: ProjectCreate) -> ProjectResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO projects (description, generalobjective, projectdocument, totalsgr, totalduration) 
                        VALUES (%s, %s, %s, %s, %s) RETURNING projectid
                        """, 
                        (project.description, project.generalobjective, project.projectdocument, project.totalsgr, project.totalduration)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return ProjectResponse(
                        id=id, 
                        description=project.description,
                        generalobjective=project.generalobjective,
                        projectdocument=project.projectdocument,
                        totalsgr=project.totalsgr,
                        totalduration=project.totalduration
                    )
        except Exception as e:
            logging.error(f"Error creating project: {e}")
            raise

    def get_projects(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM projects")
                    projects = cursor.fetchall()
                    if projects:
                        return [
                            ProjectResponse(
                                id=project[0], 
                                description=project[1],
                                generalobjective=project[2],
                                projectdocument=project[3],
                                totalsgr=project[4],
                                totalduration=project[5]
                            ) 
                            for project in projects
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching projects: {e}")
            raise

    def get_project_by_id(self, project_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM projects WHERE projectid = %s", (project_id,))
                    project = cursor.fetchone()
                    if project:
                        return ProjectResponse(
                            id=project[0], 
                            description=project[1],
                            generalobjective=project[2],
                            projectdocument=project[3],
                            totalsgr=project[4],
                            totalduration=project[5]
                        )
                    return None
        except Exception as e:
            logging.error(f"Error fetching project by id {project_id}: {e}")
            raise

    def update_project(self, project_id: int, project: ProjectCreate) -> ProjectResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE projects 
                        SET description = %s, generalobjective = %s, projectdocument = %s, totalsgr = %s, totalduration = %s 
                        WHERE projectid = %s
                        """, 
                        (project.description, project.generalobjective, project.projectdocument, project.totalsgr, project.totalduration, project_id)
                    )
                    conn.commit()
                    return ProjectResponse(
                        id=project_id, 
                        description=project.description,
                        generalobjective=project.generalobjective,
                        projectdocument=project.projectdocument,
                        totalsgr=project.totalsgr,
                        totalduration=project.totalduration
                    )
        except Exception as e:
            logging.error(f"Error updating project: {e}")
            raise

    def delete_project(self, project_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM projects WHERE projectid = %s", (project_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No project found with id {project_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting project: {e}")
            raise

    def delete_project_cascade(self, project_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("""
                        DELETE FROM taskschedule WHERE taskid IN (
                            SELECT taskid FROM tasks WHERE activityid IN (
                                SELECT activityid FROM activities WHERE specificobjectiveid IN (
                                    SELECT specificobjectiveid FROM specificobjectives WHERE projectid = %s
                                )
                            )
                        )
                    """, (project_id,))
                    
                    
                    cursor.execute("""
                        DELETE FROM tasks WHERE activityid IN (
                            SELECT activityid FROM activities WHERE specificobjectiveid IN (
                                SELECT specificobjectiveid FROM specificobjectives WHERE projectid = %s
                            )
                        )
                    """, (project_id,))
                    
                    cursor.execute("""
                        DELETE FROM activities WHERE specificobjectiveid IN (
                            SELECT specificobjectiveid FROM specificobjectives WHERE projectid = %s
                        )
                    """, (project_id,))
                    
                    cursor.execute("""
                        DELETE FROM specificobjectives WHERE projectid = %s
                    """, (project_id,))
                    
                    cursor.execute("""
                        DELETE FROM projects WHERE projectid = %s
                    """, (project_id,))
                    
                    conn.commit()
                    return True
        except Exception as e:
            logging.error(f"Error deleting project cascade: {e}")
            raise