from database.database import DatabaseConnection
from schemas.equipment_software_schema import EquipmentSoftwareSchema, EquipmentSoftwareResponse
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class EquipmentSoftwareRepository:
    def create_equipment_software(self, equipment_software: EquipmentSoftwareSchema) -> EquipmentSoftwareResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO equipmentsoftware (activityid, entity, description, justification, quantity, propertyoradministration, unitvalue, total) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING equipmentsoftwareid
                        """, 
                        (equipment_software.activity_id, equipment_software.entity, equipment_software.description, equipment_software.justification, equipment_software.quantity, equipment_software.propertyoradministration, equipment_software.unitvalue, equipment_software.total)
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return EquipmentSoftwareResponse(
                        id=id, 
                        activity_id=equipment_software.activity_id,
                        entity=equipment_software.entity,
                        description=equipment_software.description,
                        justification=equipment_software.justification,
                        quantity=equipment_software.quantity,
                        propertyoradministration=equipment_software.propertyoradministration,
                        unitvalue=equipment_software.unitvalue,
                        total=equipment_software.total
                    )
        except Exception as e:
            logging.error(f"Error creating equipment software: {e}")
            raise

    def get_equipment_softwares(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM equipmentsoftware")
                    equipment_softwares = cursor.fetchall()
                    if equipment_softwares:
                        return [
                            EquipmentSoftwareResponse(
                                id=equipment_software[0], 
                                activity_id=equipment_software[1],
                                entity=equipment_software[2],
                                description=equipment_software[3],
                                justification=equipment_software[4],
                                quantity=equipment_software[5],
                                propertyoradministration=equipment_software[6],
                                unitvalue=equipment_software[7],
                                total=equipment_software[8]
                            ) 
                            for equipment_software in equipment_softwares
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching equipment softwares: {e}")
            raise

    def get_equipment_software_by_id(self, equipment_software_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM equipmentsoftware WHERE equipmentsoftwareid = %s", (equipment_software_id,))
                    equipment_software = cursor.fetchone()
                    if equipment_software:
                        return EquipmentSoftwareResponse(
                            id=equipment_software[0], 
                            activity_id=equipment_software[1],
                            entity=equipment_software[2],
                            description=equipment_software[3],
                            justification=equipment_software[4],
                            quantity=equipment_software[5],
                            propertyoradministration=equipment_software[6],
                            unitvalue=equipment_software[7],
                            total=equipment_software[8]
                        )
                    return None
        except Exception as e:
            logging.error(f"Error fetching equipment software by id {equipment_software_id}: {e}")
            raise

    def update_equipment_software(self, equipment_software_id: int, equipment_software: EquipmentSoftwareSchema) -> EquipmentSoftwareResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE equipmentsoftware 
                        SET activityid = %s, entity = %s, description = %s, justification = %s, quantity = %s, propertyoradministration = %s, unitvalue = %s, total = %s 
                        WHERE equipmentsoftwareid = %s
                        """, 
                        (equipment_software.activity_id, equipment_software.entity, equipment_software.description, equipment_software.justification, equipment_software.quantity, equipment_software.propertyoradministration, equipment_software.unitvalue, equipment_software.total, equipment_software_id)
                    )
                    conn.commit()
                    return EquipmentSoftwareResponse(
                        id=equipment_software_id, 
                        activity_id=equipment_software.activity_id,
                        entity=equipment_software.entity,
                        description=equipment_software.description,
                        justification=equipment_software.justification,
                        quantity=equipment_software.quantity,
                        propertyoradministration=equipment_software.propertyoradministration,
                        unitvalue=equipment_software.unitvalue,
                        total=equipment_software.total
                    )
        except Exception as e:
            logging.error(f"Error updating equipment software: {e}")
            raise

    def delete_equipment_software(self, equipment_software_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("DELETE FROM equipmentsoftware WHERE equipmentsoftwareid = %s", (equipment_software_id,))
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(f"No equipment software found with id {equipment_software_id}")
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting equipment software: {e}")
            raise