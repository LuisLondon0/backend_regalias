from fastapi import APIRouter, HTTPException
from typing import List
from services.equipment_software_service import EquipmentSoftwareService
from schemas.equipment_software_schema import EquipmentSoftwareSchema, EquipmentSoftwareResponse

router = APIRouter()
service = EquipmentSoftwareService()

@router.post("/equipment_softwares", response_model=EquipmentSoftwareResponse)
def create_equipment_software(equipment_software: EquipmentSoftwareSchema):
    return service.create_equipment_software(equipment_software)

@router.get("/equipment_softwares", response_model=List[EquipmentSoftwareResponse])
def get_equipment_softwares():
    return service.get_equipment_softwares()

@router.get("/equipment_softwares/{equipment_software_id}", response_model=EquipmentSoftwareResponse)
def get_equipment_software_by_id(equipment_software_id: int):
    equipment_software = service.get_equipment_software_by_id(equipment_software_id)
    if equipment_software is None:
        raise HTTPException(status_code=404, detail="Equipment software not found")
    return equipment_software

@router.put("/equipment_softwares/{equipment_software_id}", response_model=EquipmentSoftwareResponse)
def update_equipment_software(equipment_software_id: int, equipment_software: EquipmentSoftwareSchema):
    return service.update_equipment_software(equipment_software_id, equipment_software)

@router.delete("/equipment_softwares/{equipment_software_id}", response_model=bool)
def delete_equipment_software(equipment_software_id: int):
    success = service.delete_equipment_software(equipment_software_id)
    if not success:
        raise HTTPException(status_code=404, detail="Equipment software not found")
    return success

@router.get("/generate_equipment_softwares", response_model=bool)
def generate_equipment_softwares():
    return service.generate_equipment_softwares()