from database import DatabaseConnection
from schemas.schedule_schema import ScheduleCreate, ScheduleTaskResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ScheduleRepository:
    def create_schedule(self, schedule: ScheduleCreate) -> ScheduleTaskResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO taskschedule (taskid, weekid) VALUES (%s, %s) RETURNING scheduleid",
                        (schedule.task_id, schedule.week_id)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return ScheduleTaskResponse(id=id, **schedule.model_dump())
        except Exception as e:
            logging.error(f"Error creating schedule: {e}")
            raise

    def get_schedules(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM taskschedule")
                    schedules = cursor.fetchall()
                    return [
                        ScheduleTaskResponse(id=schedule[0], task_id=schedule[1], week_id=schedule[2]) 
                        for schedule in schedules
                    ] if schedules else []
        except Exception as e:
            logging.error("Error fetching schedules: {e}")
            raise

    def get_schedule_by_id(self, schedule_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM taskschedule WHERE scheduleid = %s", (schedule_id,))
                    schedule = cursor.fetchone()
                    if schedule:
                        return ScheduleTaskResponse(id=schedule[0], task_id=schedule[1], week_id=schedule[2])
                    return None
        except Exception as e:
            logging.error(f"Error fetching schedule by id {schedule_id}: {e}")
            raise

    def update_schedule(self, schedule_id: int, schedule: ScheduleCreate) -> ScheduleTaskResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE taskschedule SET taskid = %s, weekid = %s WHERE scheduleid = %s",
                        (schedule.task_id, schedule.week_id, schedule_id)
                    )
                    conn.commit()
                    return ScheduleTaskResponse(id=schedule_id, **schedule.model_dump())
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
