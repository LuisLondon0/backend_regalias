from database import DatabaseConnection
from schemas.general_objective_schema import GeneralObjectiveCreate, GeneralObjectiveResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GeneralObjectiveRepository:
    def create_general_objective(self, general_objective: GeneralObjectiveCreate) -> GeneralObjectiveResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO generalobjective (description) VALUES (%s) RETURNING uniqueid", 
                        (general_objective.description,)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return GeneralObjectiveResponse(id=id, description=general_objective.description)
        except Exception as e:
            logging.error(f"Error creating general objective: {e}")
            raise

    def get_general_objectives(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM generalobjective")
                    general_objectives = cursor.fetchall()
                    if general_objectives:
                        return [
                            GeneralObjectiveResponse(id=general_objective[0], description=general_objective[1]) 
                            for general_objective in general_objectives
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching general objectives: {e}")
            raise

    def get_general_objective_by_id(self, general_objective_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM generalobjective WHERE uniqueid = %s", (general_objective_id,))
                    general_objective = cursor.fetchone()
                    if general_objective:
                        return GeneralObjectiveResponse(id=general_objective[0], description=general_objective[1])
                    return None
        except Exception as e:
            logging.error(f"Error fetching general objective by id {general_objective_id}: {e}")
            raise

    def update_general_objective(self, general_objective_id: int, general_objective: GeneralObjectiveCreate) -> GeneralObjectiveResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE generalobjective SET description = %s WHERE uniqueid = %s", 
                        (general_objective.description, general_objective_id)
                    )
                    conn.commit()
                    return GeneralObjectiveResponse(id=general_objective_id, description=general_objective.description)
        except Exception as e:
            logging.error(f"Error updating general objective: {e}")
            raise

    def delete_general_objective(self, general_objective_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM generalobjective WHERE uniqueid = %s", (general_objective_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No general objective found with id {general_objective_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting general objective: {e}")
            raise