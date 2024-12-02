from database.database import DatabaseConnection
from schemas.sgr_schema import SGRSchema, SGRResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SGRRepository:
    def create_sgr(self, sgr: SGRSchema) -> SGRResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO sgr (resourceid, resourcetype, cash) 
                        VALUES (%s, %s, %s) RETURNING counterpartid
                        """, 
                        (sgr.resourceid, sgr.resourcetype, sgr.cash)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return SGRResponse(
                        id=id, 
                        resourceid=sgr.resourceid,
                        resourcetype=sgr.resourcetype,
                        cash=sgr.cash
                    )
        except Exception as e:
            logging.error(f"Error creating SGR: {e}")
            raise

    def get_sgrs(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM sgr")
                    sgrs = cursor.fetchall()
                    if sgrs:
                        return [
                            SGRResponse(
                                id=sgr[0], 
                                resourceid=sgr[1],
                                resourcetype=sgr[2],
                                cash=sgr[3]
                            ) 
                            for sgr in sgrs
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching SGRs: {e}")
            raise

    def get_sgr_by_id(self, sgr_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM sgr WHERE counterpartid = %s", (sgr_id,))
                    sgr = cursor.fetchone()
                    if sgr:
                        return SGRResponse(
                            id=sgr[0], 
                            resourceid=sgr[1],
                            resourcetype=sgr[2],
                            cash=sgr[3]
                        )
                    return None
        except Exception as e:
            logging.error(f"Error fetching SGR by id {sgr_id}: {e}")
            raise

    def update_sgr(self, sgr_id: int, sgr: SGRSchema) -> SGRResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE sgr 
                        SET resourceid = %s, resourcetype = %s, cash = %s 
                        WHERE counterpartid = %s
                        """, 
                        (sgr.resourceid, sgr.resourcetype, sgr.cash, sgr_id)
                    )
                    conn.commit()
                    return SGRResponse(
                        id=sgr_id, 
                        resourceid=sgr.resourceid,
                        resourcetype=sgr.resourcetype,
                        cash=sgr.cash
                    )
        except Exception as e:
            logging.error(f"Error updating SGR: {e}")
            raise

    def delete_sgr(self, sgr_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM sgr WHERE counterpartid = %s", (sgr_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No SGR found with id {sgr_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting SGR: {e}")
            raise