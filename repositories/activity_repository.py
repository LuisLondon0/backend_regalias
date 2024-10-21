from database import DatabaseConnection
from schemas.activity_schema import ActivityCreate, ActivityResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ActivityRepository:
    def create_activity(self, activity: ActivityCreate) -> ActivityResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "INSERT INTO activities (specificobjectiveid, description, product, verificationmethod, productindicator) VALUES (%s, %s, %s, %s, %s) RETURNING uniqueid", 
                        (activity.specific_objective_id, activity.description, activity.product, activity.verification_method, activity.product_indicator)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return ActivityResponse(id=id, **activity.model_dump())
        except Exception as e:
            logging.error(f"Error creating activity: {e}")
            raise

    def get_activities(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM activities")
                    activities = cursor.fetchall()
                    if activities:
                        return [
                            ActivityResponse(id=activity[0], specific_objective_id=activity[1], description=activity[2], product=activity[3], verification_method=activity[4], product_indicator=activity[5]) 
                            for activity in activities
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching activities: {e}")
            raise

    def get_activity_by_id(self, activity_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM activities WHERE uniqueid = %s", (activity_id,))
                    activity = cursor.fetchone()
                    if activity:
                        return ActivityResponse(id=activity[0], specific_objective_id=activity[1], description=activity[2], product=activity[3], verification_method=activity[4], product_indicator=activity[5])
                    return None
        except Exception as e:
            logging.error(f"Error fetching activity by id {activity_id}: {e}")
            raise

    def update_activity(self, activity_id: int, activity: ActivityCreate) -> ActivityResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "UPDATE activities SET specificobjectiveid = %s, description = %s, product = %s, verificationmethod = %s, productindicator = %s WHERE uniqueid = %s", 
                        (activity.specific_objective_id, activity.description, activity.product, activity.verification_method, activity.product_indicator, activity_id)
                    )
                    conn.commit()
                    return ActivityResponse(id=activity_id, **activity.model_dump())
        except Exception as e:
            logging.error(f"Error updating activity: {e}")
            raise

    def delete_activity(self, activity_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM activities WHERE uniqueid = %s", (activity_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No activity found with id {activity_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting activity: {e}")
            raise