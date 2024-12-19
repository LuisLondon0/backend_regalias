from database.database import DatabaseConnection
from schemas.training_events_schema import (
    TrainingEventSchema,
    TrainingEventResponse,
)
import logging

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


class TrainingEventRepository:
    def get_training_events(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM trainingevents")
                    training_events = cursor.fetchall()
                    if training_events:
                        return [
                            TrainingEventResponse(
                                id=training_event[0],
                                activity_id=training_event[1],
                                entity=training_event[2],
                                theme=training_event[3],
                                justification=training_event[4],
                                quantity=training_event[5],
                                total=training_event[6],
                            )
                            for training_event in training_events
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching training_event s: {e}")
            raise

    def create_training_event(
        self, training_event: TrainingEventSchema
    ) -> TrainingEventResponse:
        pass

        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO trainingevents (entity, theme, justification, quantity, total, activityid)
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING trainingeventid
                        """,
                        (
                            training_event.entity,
                            training_event.theme,
                            training_event.justification,
                            training_event.quantity,
                            training_event.total,
                            training_event.activity_id,
                        ),
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return TrainingEventResponse(
                        id=id,
                        entity=training_event.entity,
                        theme=training_event.theme,
                        justification=training_event.justification,
                        quantity=training_event.quantity,
                        total=training_event.total,
                        activity_id=training_event.activity_id,
                    )
        except Exception as e:
            logging.error(f"Error creating training_event : {e}")
            raise

    def get_training_event_by_id(self, training_event_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM trainingevents WHERE trainingeventid = %s",
                        (training_event_id,),
                    )
                    training_event = cursor.fetchone()
                    if training_event:
                        return TrainingEventResponse(
                            id=training_event[0],
                            activity_id=training_event[1],
                            entity=training_event[2],
                            theme=training_event[3],
                            justification=training_event[4],
                            quantity=training_event[5],
                            total=training_event[6],
                        )
                    return None
        except Exception as e:
            logging.error(
                f"Error fetching training_event by id {training_event_id}: {e}"
            )
            raise

    def update_training_event(
        self, training_event_id: int, training_event: TrainingEventSchema
    ) -> TrainingEventResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE trainingevents
                            SET activityid = %s, entity = %s, theme = %s, 
                            justification = %s, quantity = %s, total = %s
                        WHERE trainingeventid = %s
                        """,
                        (
                            training_event.activity_id,
                            training_event.entity,
                            training_event.theme,
                            training_event.justification,
                            training_event.quantity,
                            training_event.total,
                            training_event_id,
                        ),
                    )
                    conn.commit()
                    return TrainingEventResponse(
                        id=training_event_id,
                        activity_id=training_event.activity_id,
                        entity=training_event.entity,
                        theme=training_event.theme,
                        justification=training_event.justification,
                        quantity=training_event.quantity,
                        total=training_event.total,
                    )
        except Exception as e:
            logging.error(f"Error updating training_event : {e}")
            raise

    def delete_training_event(self, training_event_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM trainingevents WHERE trainingeventid = %s",
                        (training_event_id,),
                    )
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(
                            f"No training_event found with id {training_event_id}"
                        )
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting training_event : {e}")
            raise
