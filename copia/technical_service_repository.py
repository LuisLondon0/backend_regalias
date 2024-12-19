from database.database import DatabaseConnection
from schemas.technical_services_schemas import (
    TechnicalServiceSchema,
    TechnicalServiceResponse,
)
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


class TechnicalServiceRepository:
    def get_technical_services(self):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute("SELECT * FROM technicalservices")
                    technical_services = cursor.fetchall()
                    print(f"{technical_services=}")

                    if technical_services:
                        return [
                            TechnicalServiceResponse(
                                id=technical_service[0],
                                activity_id=technical_service[1],
                                entity=technical_service[2],
                                test_services=technical_service[3],
                                description=technical_service[4],
                                tech_specification=technical_service[5],
                                quantity=technical_service[6],
                                unitvalue=technical_service[7],
                                cost=technical_service[8],
                            )
                            for technical_service in technical_services
                        ]
                    else:
                        return []
        except Exception as e:
            logging.error(f"Error fetching equipment softwares: {e}")
            raise

    def create_technical_service(
        self, technical_service: TechnicalServiceSchema
    ) -> TechnicalServiceResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        INSERT INTO technicalservices (
                            activityid, entity, servicetests, description,
                            technicalspecification, quantity, unitvalue, cost
                        )
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s) RETURNING serviceid
                        """,
                        (
                            technical_service.activity_id,
                            technical_service.entity,
                            technical_service.test_services,
                            technical_service.description,
                            technical_service.tech_specification,
                            technical_service.quantity,
                            technical_service.unitvalue,
                            technical_service.cost,
                        ),
                    )
                    row = cursor.fetchone()
                    id = row[0] if row else None
                    conn.commit()
                    return TechnicalServiceResponse(
                        id=id,
                        activity_id=technical_service.activity_id,
                        entity=technical_service.entity,
                        test_services=technical_service.test_services,
                        description=technical_service.description,
                        tech_specification=technical_service.tech_specification,
                        quantity=technical_service.quantity,
                        unitvalue=technical_service.unitvalue,
                        cost=technical_service.cost,
                    )
        except Exception as e:
            logging.error(f"Error creating equipment software: {e}")
            raise

    def get_technical_service_by_id(self, technical_service_id: int):
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "SELECT * FROM technicalservices WHERE serviceid = %s",
                        (technical_service_id,),
                    )
                    technical_service = cursor.fetchone()
                    if technical_service:
                        return TechnicalServiceResponse(
                            id=technical_service[0],
                            activity_id=technical_service[1],
                            entity=technical_service[2],
                            test_services=technical_service[3],
                            description=technical_service[4],
                            tech_specification=technical_service[5],
                            quantity=technical_service[6],
                            unitvalue=technical_service[7],
                            cost=technical_service[8],
                        )
                    return None
        except Exception as e:
            logging.error(
                f"Error fetching technical service by id {technical_service_id}: {e}"
            )
            raise

    def update_technical_service(
        self, technical_service_id: int, technical_service: TechnicalServiceSchema
    ) -> TechnicalServiceResponse:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """
                        UPDATE technicalservices
                        SET activityid = %s, entity = %s, servicetests = %s, 
                            description = %s, technicalspecification = %s, 
                            quantity = %s, unitvalue = %s, cost = %s
                        WHERE serviceid = %s
                        """,
                        (
                            technical_service.activity_id,
                            technical_service.entity,
                            technical_service.test_services,
                            technical_service.description,
                            technical_service.tech_specification,
                            technical_service.quantity,
                            technical_service.unitvalue,
                            technical_service.cost,
                            technical_service_id,
                        ),
                    )
                    conn.commit()
                    return TechnicalServiceResponse(
                        id=technical_service_id,
                        activity_id=technical_service.activity_id,
                        entity=technical_service.entity,
                        test_services=technical_service.test_services,
                        description=technical_service.description,
                        tech_specification=technical_service.tech_specification,
                        quantity=technical_service.quantity,
                        unitvalue=technical_service.unitvalue,
                        cost=technical_service.cost,
                    )
        except Exception as e:
            logging.error(f"Error updating technical service: {e}")
            raise

    def delete_technical_service(self, technical_service_id: int) -> bool:
        try:
            with DatabaseConnection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(
                        "DELETE FROM technicalservices WHERE serviceid = %s",
                        (technical_service_id,),
                    )
                    conn.commit()
                    if cursor.rowcount == 0:
                        logging.warning(
                            f"No technical service found with id {technical_service_id}"
                        )
                        return False
                    return True
        except Exception as e:
            logging.error(f"Error deleting technical service: {e}")
            raise
