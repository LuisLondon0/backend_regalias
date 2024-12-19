from repositories.technical_service_repository import TechnicalServiceRepository
from schemas.technical_services_schemas import (
    TechnicalServiceSchema,
    TechnicalServiceResponse,
)
from services.activity_service import ActivityService
import logging


class TechnicalServiceService:
    def __init__(self):
        self.repo = TechnicalServiceRepository()
        self.activity_service = ActivityService()

    def assign_fields(self, technical_service: TechnicalServiceSchema):
        technical_service.entity = technical_service.entity.strip()
        technical_service.test_services = technical_service.test_services.strip()
        technical_service.description = technical_service.description.strip()
        technical_service.tech_specification = (
            technical_service.tech_specification.strip()
        )
        technical_service.quantity = technical_service.quantity
        technical_service.unitvalue = technical_service.unitvalue
        technical_service.cost = technical_service.cost
        return technical_service

    def validate_fields(self, technical_service: TechnicalServiceSchema, activity):
        if not activity:
            raise ValueError("Activity does not exist")
        if not technical_service.entity:
            raise ValueError("Entity cannot be empty")
        if not technical_service.test_services:
            raise ValueError("Test services cannot be empty")
        if not technical_service.description:
            raise ValueError("Description cannot be empty")
        if not technical_service.tech_specification:
            raise ValueError("Technical specification cannot be empty")
        if not technical_service.quantity > 0:
            raise ValueError("Quantity must be a positive integer")
        if technical_service.unitvalue < 0:
            raise ValueError("Unit value cannot be negative")
        if technical_service.cost < 0:
            raise ValueError("Cost cannot be negative")

    def get_technical_services(self):
        return self.repo.get_technical_services()

    def create_technical_service(
        self, technical_service: TechnicalServiceSchema
    ) -> TechnicalServiceResponse:
        activity = self.activity_service.get_activity_by_id(
            technical_service.activity_id,
        )

        self.validate_fields(technical_service, activity)
        technical_service = self.assign_fields(technical_service)

        response = self.repo.create_technical_service(technical_service)
        logging.info(f"Technical services created with ID: {response.id}")

        return response

    def get_technical_service_by_id(self, technical_service_id: int):
        if not technical_service_id > 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_technical_service_by_id(technical_service_id)

    def update_technical_service(
        self, technical_service_id: int, technical_service: TechnicalServiceSchema
    ) -> TechnicalServiceResponse:
        activity = self.activity_service.get_activity_by_id(
            technical_service.activity_id
        )

        self.validate_fields(technical_service, activity)
        technical_service = self.assign_fields(technical_service)

        response = self.repo.update_technical_service(
            technical_service_id, technical_service
        )

        logging.info(f"Technical service with ID: {technical_service_id} updated")

        return response

    def delete_technical_service(self, technical_service_id: int) -> bool:
        if not technical_service_id > 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_technical_service(technical_service_id)

        if success:
            logging.info(f"Technical service with ID: {technical_service_id} deleted")
        else:
            logging.warning(
                f"Technical service with ID: {technical_service_id} not found"
            )

        return success
