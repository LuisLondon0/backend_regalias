from database import DatabaseConnection
from schemas.human_talent_schema import HumanTalentCreate, HumanTalentResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class HumanTalentRepository:
    def create_human_talent(self, human_talent: HumanTalentCreate) -> HumanTalentResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO humantalent (activityid, feevalueid, entity, position, justification, quantity) 
                        VALUES (%s, %s, %s, %s, %s, %s) RETURNING talentid
                        """, 
                        (human_talent.activityid, human_talent.feevalueid, human_talent.entity, human_talent.position, human_talent.justification, human_talent.quantity)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return HumanTalentResponse(
                        id=id, 
                        activityid=human_talent.activityid,
                        feevalueid=human_talent.feevalueid,
                        entity=human_talent.entity,
                        position=human_talent.position,
                        justification=human_talent.justification,
                        quantity=human_talent.quantity
                    )
        except Exception as e:
            logging.error(f"Error creating human talent: {e}")
            raise

    def get_human_talents(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM humantalent")
                    human_talents = cursor.fetchall()
                    if human_talents:
                        return [
                            HumanTalentResponse(
                                id=human_talent[0], 
                                activityid=human_talent[1],
                                feevalueid=human_talent[2],
                                entity=human_talent[3],
                                position=human_talent[4],
                                justification=human_talent[5],
                                quantity=human_talent[6]
                            ) 
                            for human_talent in human_talents
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching human talents: {e}")
            raise

    def get_human_talent_by_id(self, human_talent_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM humantalent WHERE talentid = %s", (human_talent_id,))
                    human_talent = cursor.fetchone()
                    if human_talent:
                        return HumanTalentResponse(
                            id=human_talent[0], 
                            activityid=human_talent[1],
                            feevalueid=human_talent[2],
                            entity=human_talent[3],
                            position=human_talent[4],
                            justification=human_talent[5],
                            quantity=human_talent[6]
                        )
                    return None
        except Exception as e:
            logging.error(f"Error fetching human talent by id {human_talent_id}: {e}")
            raise

    def update_human_talent(self, human_talent_id: int, human_talent: HumanTalentCreate) -> HumanTalentResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE humantalent 
                        SET activityid = %s, feevalueid = %s, entity = %s, position = %s, justification = %s, quantity = %s 
                        WHERE talentid = %s
                        """, 
                        (human_talent.activityid, human_talent.feevalueid, human_talent.entity, human_talent.position, human_talent.justification, human_talent.quantity, human_talent_id)
                    )
                    conn.commit()
                    return HumanTalentResponse(
                        id=human_talent_id, 
                        activityid=human_talent.activityid,
                        feevalueid=human_talent.feevalueid,
                        entity=human_talent.entity,
                        position=human_talent.position,
                        justification=human_talent.justification,
                        quantity=human_talent.quantity
                    )
        except Exception as e:
            logging.error(f"Error updating human talent: {e}")
            raise

    def delete_human_talent(self, human_talent_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM humantalent WHERE talentid = %s", (human_talent_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No human talent found with id {human_talent_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting human talent: {e}")
            raise