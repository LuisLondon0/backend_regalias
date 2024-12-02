from database.database import DatabaseConnection
from schemas.counterpart_schema import CounterpartSchema, CounterpartResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class CounterpartRepository:
    def create_counterpart(self, counterpart: CounterpartSchema) -> CounterpartResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO counterpart (resourceid, resourcetype, entity, inkind, cash) 
                        VALUES (%s, %s, %s, %s, %s) RETURNING counterpartid
                        """, 
                        (counterpart.resourceid, counterpart.resorucetype, counterpart.entity, counterpart.inkind, counterpart.cash)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return CounterpartResponse(
                        id=id, 
                        resourceid=counterpart.resourceid,
                        resorucetype=counterpart.resorucetype,
                        entity=counterpart.entity,
                        inkind=counterpart.inkind,
                        cash=counterpart.cash
                    )
        except Exception as e:
            logging.error(f"Error creating counterpart: {e}")
            raise

    def get_counterparts(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM counterpart")
                    counterparts = cursor.fetchall()
                    if counterparts:
                        return [
                            CounterpartResponse(
                                id=counterpart[0], 
                                resourceid=counterpart[1],
                                resorucetype=counterpart[2],
                                entity=counterpart[3],
                                inkind=counterpart[4],
                                cash=counterpart[5]
                            ) 
                            for counterpart in counterparts
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching counterparts: {e}")
            raise

    def get_counterpart_by_id(self, counterpart_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM counterpart WHERE counterpartid = %s", (counterpart_id,))
                    counterpart = cursor.fetchone()
                    if counterpart:
                        return CounterpartResponse(
                            id=counterpart[0], 
                            resourceid=counterpart[1],
                            resorucetype=counterpart[2],
                            entity=counterpart[3],
                            inkind=counterpart[4],
                            cash=counterpart[5]
                        )
                    return None
        except Exception as e:
            logging.error(f"Error fetching counterpart by id {counterpart_id}: {e}")
            raise

    def update_counterpart(self, counterpart_id: int, counterpart: CounterpartSchema) -> CounterpartResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE counterpart 
                        SET resourceid = %s, resourcetype = %s, entity = %s, inkind = %s, cash = %s 
                        WHERE counterpartid = %s
                        """, 
                        (counterpart.resourceid, counterpart.resorucetype, counterpart.entity, counterpart.inkind, counterpart.cash, counterpart_id)
                    )
                    conn.commit()
                    return CounterpartResponse(
                        id=counterpart_id, 
                        resourceid=counterpart.resourceid,
                        resorucetype=counterpart.resorucetype,
                        entity=counterpart.entity,
                        inkind=counterpart.inkind,
                        cash=counterpart.cash
                    )
        except Exception as e:
            logging.error(f"Error updating counterpart: {e}")
            raise

    def delete_counterpart(self, counterpart_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM counterpart WHERE counterpartid = %s", (counterpart_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No counterpart found with id {counterpart_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting counterpart: {e}")
            raise