from database.database import DatabaseConnection
from schemas.schedule_schema import ScheduleCreate, ScheduleResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScheduleRepository:
    def create_schedule(self, schedule: ScheduleCreate) -> ScheduleResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO taskschedule (taskid, monthid) VALUES (%s, %s) RETURNING scheduleid", 
                        (schedule.task_id, schedule.month_id)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return ScheduleResponse(id=id, task_id=schedule.task_id, month_id=schedule.month_id)
        except Exception as e:
            logging.error(f"Error creating schedule: {e}")
            raise

    def get_schedules(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM taskschedule")
                    schedules = cursor.fetchall()
                    if schedules:
                        return [
                            ScheduleResponse(id=schedule[0], task_id=schedule[1], month_id=schedule[2]) 
                            for schedule in schedules
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching schedules: {e}")
            raise

    def get_schedule_by_id(self, schedule_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM taskschedule WHERE scheduleid = %s", (schedule_id,))
                    schedule = cursor.fetchone()
                    if schedule:
                        return ScheduleResponse(id=schedule[0], task_id=schedule[1], month_id=schedule[2])
                    return None
        except Exception as e:
            logging.error(f"Error fetching schedule by id {schedule_id}: {e}")
            raise

    def get_schedules_by_month_id(self, month_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM taskschedule WHERE monthid = %s", (month_id,))
                    schedules = cursor.fetchall()
                    if schedules:
                        return [
                            ScheduleResponse(id=schedule[0], task_id=schedule[1], month_id=schedule[2]) 
                            for schedule in schedules
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching schedules by month_id {month_id}: {e}")
            raise

    def get_schedules_by_task_id(self, task_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM taskschedule WHERE taskid = %s", (task_id,))
                    schedules = cursor.fetchall()
                    if schedules:
                        return [
                            ScheduleResponse(id=schedule[0], task_id=schedule[1], month_id=schedule[2]) 
                            for schedule in schedules
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching schedules by task_id {task_id}: {e}")
            raise

    def update_schedule(self, schedule_id: int, schedule: ScheduleCreate) -> ScheduleResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE taskschedule SET taskid = %s, monthid = %s WHERE scheduleid = %s", 
                        (schedule.task_id, schedule.month_id, schedule_id)
                    )
                    conn.commit()
                    return ScheduleResponse(id=schedule_id, task_id=schedule.task_id, month_id=schedule.month_id)
        except Exception as e:
            logging.error(f"Error updating schedule: {e}")
            raise

    def delete_schedule(self, schedule_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM taskschedule WHERE scheduleid = %s", (schedule_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No schedule found with id {schedule_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting schedule: {e}")
            raise
    
    def check_schedule_exists(self, task_id: int, month_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM taskschedule WHERE taskid = %s AND monthid = %s",
                        (task_id, month_id)
                    )
                    return cursor.fetchone() is not None
        except Exception as e:
            logging.error(f"Error checking if schedule exists: {e}")
            raise