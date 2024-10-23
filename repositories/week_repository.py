from database import DatabaseConnection
from schemas.week_schema import WeekCreate, WeekResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class WeekRepository:
    def create_week(self, week: WeekCreate) -> WeekResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO weeks (week) VALUES (%s) RETURNING uniqueid", 
                        (week.week,)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return WeekResponse(id=id, week=week.week)
        except Exception as e:
            logging.error(f"Error creating week: {e}")
            raise

    def get_weeks(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM weeks")
                    weeks = cursor.fetchall()
                    if weeks:
                        return [
                            WeekResponse(id=week[0], week=week[1]) 
                            for week in weeks
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching weeks: {e}")
            raise

    def get_week_by_id(self, week_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM weeks WHERE uniqueid = %s", (week_id,))
                    week = cursor.fetchone()
                    if week:
                        return WeekResponse(id=week[0], week=week[1])
                    return None
        except Exception as e:
            logging.error(f"Error fetching week by id {week_id}: {e}")
            raise

    def update_week(self, week_id: int, week: WeekCreate) -> WeekResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE weeks SET week = %s WHERE id = %s", 
                        (week.week, week_id)
                    )
                    conn.commit()
                    return WeekResponse(id=week_id, week=week.week)
        except Exception as e:
            logging.error(f"Error updating week: {e}")
            raise

    def delete_week(self, week_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM weeks WHERE uniqueid = %s", (week_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No week found with id {week_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting week: {e}")
            raise