from database import DatabaseConnection
from schemas.task_schema import TaskCreate, TaskResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class TaskRepository:
    def create_task(self, task: TaskCreate) -> TaskResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO tasks (activityid, description, responsible, requiredpersonnel, activityresults, technicalrequirements) VALUES (%s, %s, %s, %s, %s, %s) RETURNING taskid", 
                        (task.activity_id, task.description, task.responsible, task.required_personnel, task.activity_results, task.technical_requirement)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return TaskResponse(id=id, **task.model_dump())
        except Exception as e:
            logging.error(f"Error creating task: {e}")
            raise

    def get_tasks(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM tasks")
                    tasks = cursor.fetchall()
                    if tasks:
                        return [
                            TaskResponse(id=task[0], activity_id=task[1], description=task[2], responsible=task[3], required_personnel=task[4], activity_results=task[5], technical_requirement=task[6]) 
                            for task in tasks
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching tasks: {e}")
            raise

    def get_task_by_id(self, task_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM tasks WHERE taskid = %s", (task_id,))
                    task = cursor.fetchone()
                    if task:
                        return TaskResponse(id=task[0], activity_id=task[1], description=task[2], responsible=task[3], required_personnel=task[4], activity_results=task[5], technical_requirement=task[6])
                    return None
        except Exception as e:
            logging.error(f"Error fetching task by id {task_id}: {e}")
            raise

    def update_task(self, task_id: int, task: TaskCreate) -> TaskResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE tasks SET activityid = %s, description = %s, responsible = %s, requiredpersonnel = %s, activityresults = %s, technicalrequirements = %s WHERE taskid = %s", 
                        (task.activity_id, task.description, task.responsible, task.required_personnel, task.activity_results, task.technical_requirement, task_id)
                    )
                    conn.commit()
                    return TaskResponse(id=task_id, **task.model_dump())
        except Exception as e:
            logging.error(f"Error updating task: {e}")
            raise

    def delete_task(self, task_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM tasks WHERE taskid = %s", (task_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No task found with id {task_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting task: {e}")
            raise