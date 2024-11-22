from database import DatabaseConnection
from schemas.specific_objective_schema import SpecificObjectiveCreate, SpecificObjectiveResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SpecificObjectiveRepository:
    def create_specific_objective(self, specific_objective: SpecificObjectiveCreate) -> SpecificObjectiveResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO specificobjectives (description, projectid) VALUES (%s, %s) RETURNING specificobjectiveid", 
                        (specific_objective.description, specific_objective.project_id)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return SpecificObjectiveResponse(id=id, description=specific_objective.description, project_id=specific_objective.project_id)
        except Exception as e:
            logging.error(f"Error creating specific objective: {e}")
            raise

    def get_specific_objectives(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM specificobjectives")
                    specific_objectives = cursor.fetchall()
                    if specific_objectives:
                        return [
                            SpecificObjectiveResponse(id=specific_objective[0], description=specific_objective[1], project_id=specific_objective[2]) 
                            for specific_objective in specific_objectives
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching specific objectives: {e}")
            raise

    def get_specific_objective_by_id(self, specific_objective_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM specificobjectives WHERE specificobjectiveid = %s", (specific_objective_id,))
                    specific_objective = cursor.fetchone()
                    if specific_objective:
                        return SpecificObjectiveResponse(id=specific_objective[0], description=specific_objective[1], project_id=specific_objective[2])
                    return None
        except Exception as e:
            logging.error(f"Error fetching specific objective by id {specific_objective_id}: {e}")
            raise

    def update_specific_objective(self, specific_objective_id: int, specific_objective: SpecificObjectiveCreate) -> SpecificObjectiveResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE specificobjectives SET description = %s, projectid = %s WHERE specificobjectiveid = %s", 
                        (specific_objective.description, specific_objective.project_id, specific_objective_id)
                    )
                    conn.commit()
                    return SpecificObjectiveResponse(id=specific_objective_id, description=specific_objective.description, project_id=specific_objective.project_id)
        except Exception as e:
            logging.error(f"Error updating specific objective: {e}")
            raise

    def delete_specific_objective(self, specific_objective_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM specificobjectives WHERE specificobjectiveid = %s", (specific_objective_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No specific objective found with id {specific_objective_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting specific objective: {e}")
            raise