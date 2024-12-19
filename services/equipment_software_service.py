from repositories.equipment_software_repository import EquipmentSoftwareRepository
from schemas.equipment_software_schema import EquipmentSoftwareSchema, EquipmentSoftwareResponse
from services.activity_service import ActivityService
import logging

class EquipmentSoftwareService:
    def __init__(self):
        self.repo = EquipmentSoftwareRepository()
        self.activity_service = ActivityService()

    def create_equipment_software(self, equipment_software: EquipmentSoftwareSchema) -> EquipmentSoftwareResponse:
        activity = self.activity_service.get_activity_by_id(equipment_software.activity_id)
        if not activity:
            raise ValueError("Activity does not exist")

        if not equipment_software.entity:
            raise ValueError("Entity cannot be empty")
        if not equipment_software.description:
            raise ValueError("Description cannot be empty")
        if not equipment_software.justification:
            raise ValueError("Justification cannot be empty")
        if equipment_software.quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        if equipment_software.unitvalue < 0:
            raise ValueError("Unit value cannot be negative")
        if equipment_software.total < 0:
            raise ValueError("Total value cannot be negative")

        equipment_software.entity = equipment_software.entity.strip()
        equipment_software.description = equipment_software.description.strip()
        equipment_software.justification = equipment_software.justification.strip()
        equipment_software.propertyoradministration = equipment_software.propertyoradministration.strip()

        response = self.repo.create_equipment_software(equipment_software)

        logging.info(f"Equipment software created with ID: {response.id}")

        return response

    def get_equipment_softwares(self):
        return self.repo.get_equipment_softwares()

    def get_equipment_software_by_id(self, equipment_software_id: int):
        if equipment_software_id <= 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_equipment_software_by_id(equipment_software_id)

    def update_equipment_software(self, equipment_software_id: int, equipment_software: EquipmentSoftwareSchema) -> EquipmentSoftwareResponse:
        activity = self.activity_service.get_activity_by_id(equipment_software.activity_id)
        if not activity:
            raise ValueError("Activity does not exist")

        if not equipment_software.entity:
            raise ValueError("Entity cannot be empty")
        if not equipment_software.description:
            raise ValueError("Description cannot be empty")
        if not equipment_software.justification:
            raise ValueError("Justification cannot be empty")
        if equipment_software.quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        if equipment_software.unitvalue < 0:
            raise ValueError("Unit value cannot be negative")
        if equipment_software.total < 0:
            raise ValueError("Total value cannot be negative")

        equipment_software.entity = equipment_software.entity.strip()
        equipment_software.description = equipment_software.description.strip()
        equipment_software.justification = equipment_software.justification.strip()
        equipment_software.propertyoradministration = equipment_software.propertyoradministration.strip()

        response = self.repo.update_equipment_software(equipment_software_id, equipment_software)

        logging.info(f"Equipment software with ID: {equipment_software_id} updated")

        return response

    def delete_equipment_software(self, equipment_software_id: int) -> bool:
        if equipment_software_id <= 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_equipment_software(equipment_software_id)

        if success:
            logging.info(f"Equipment software with ID: {equipment_software_id} deleted")
        else:
            logging.warning(f"Equipment software with ID: {equipment_software_id} not found")

        return success
    

    def generate_equipment_softwares(self):
        return self.repo.generate_equipment_softwares()
    
    def get_equipment_software_by_project_id(self, project_id: int):
        if project_id <= 0:
            raise ValueError("ID must be a positive integer")
        
        return self.repo.get_equipment_software_by_project_id(project_id)