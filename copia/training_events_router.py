from fastapi import APIRouter, HTTPException
from typing import List
from services.training_events_service import TrainingEventService
from schemas.training_events_schema import (
    TrainingEventSchema,
    TrainingEventResponse,
)

router = APIRouter()
service = TrainingEventService()


@router.post(
    "/training_events",
    response_model=TrainingEventResponse,
)
def create_training_event(equipment_software: TrainingEventSchema):
    return service.create_training_event(equipment_software)


@router.get(
    "/training_events",
    response_model=list[TrainingEventResponse],
)
def get_training_events():
    return service.get_training_events()


@router.get(
    "/training_events/{equipment_software_id}",
    response_model=TrainingEventResponse,
)
def get_training_event_by_id(equipment_software_id: int):
    equipment_software = service.get_training_event_by_id(equipment_software_id)
    if equipment_software is None:
        raise HTTPException(status_code=404, detail="Training event not found")
    return equipment_software


@router.put(
    "/training_events/{equipment_software_id}",
    response_model=TrainingEventResponse,
)
def update_training_event(
    equipment_software_id: int, equipment_software: TrainingEventSchema
):
    return service.update_training_event(
        equipment_software_id,
        equipment_software,
    )


@router.delete(
    "/training_events/{equipment_software_id}",
    response_model=bool,
)
def delete_training_event(equipment_software_id: int):
    success = service.delete_training_event(equipment_software_id)
    if not success:
        raise HTTPException(status_code=404, detail="Training event not found")
    return success
