from database import DatabaseConnection
from schemas.month_schema import MonthCreate, MonthResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class MonthRepository:
    def create_month(self, month: MonthCreate) -> MonthResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO months (month) VALUES (%s) RETURNING monthid", 
                        (month.month,)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return MonthResponse(id=id, month=month.month)
        except Exception as e:
            logging.error(f"Error creating month: {e}")
            raise

    def get_months(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM months")
                    months = cursor.fetchall()
                    if months:
                        return [
                            MonthResponse(id=month[0], month=month[1]) 
                            for month in months
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching months: {e}")
            raise

    def get_month_by_id(self, month_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM months WHERE monthid = %s", (month_id,))
                    month = cursor.fetchone()
                    if month:
                        return MonthResponse(id=month[0], month=month[1])
                    return None
        except Exception as e:
            logging.error(f"Error fetching month by id {month_id}: {e}")
            raise

    def update_month(self, month_id: int, month: MonthCreate) -> MonthResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE months SET month = %s WHERE monthid = %s", 
                        (month.month, month_id)
                    )
                    conn.commit()
                    return MonthResponse(id=month_id, month=month.month)
        except Exception as e:
            logging.error(f"Error updating month: {e}")
            raise

    def delete_month(self, month_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM months WHERE monthid = %s", (month_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No month found with id {month_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting month: {e}")
            raise