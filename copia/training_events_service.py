from repositories.training_events_repository import TrainingEventRepository
from schemas.training_events_schema import (
    TrainingEventSchema,
    TrainingEventResponse,
)
from services.activity_service import ActivityService
import logging


class TrainingEventService:
    def __init__(self):
        self.repo = TrainingEventRepository()
        self.activity_service = ActivityService()

    def create_training_event(
        self, training_event: TrainingEventSchema
    ) -> TrainingEventResponse:
        activity = self.activity_service.get_activity_by_id(training_event.activity_id)

        self.validate_fields(training_event, activity)
        training_event = self.assign_fields(training_event)

        response = self.repo.create_training_event(training_event)
        logging.info(f"ttaining event created with ID: {response.id}")

        return response

    def get_training_events(self):
        return self.repo.get_training_events()

    def assign_fields(self, training_event: TrainingEventSchema):
        training_event.entity = training_event.entity.strip()
        training_event.theme = training_event.theme.strip()
        training_event.justification = training_event.justification.strip()
        training_event.quantity = training_event.quantity
        training_event.total = training_event.total
        return training_event

    def validate_fields(self, training_event, activity):
        if not activity:
            raise ValueError("Activity does not exist")
        if not training_event.entity:
            raise ValueError("Entity cannot be empty")
        if not training_event.theme:
            raise ValueError("Theme cannot be empty")
        if not training_event.justification:
            raise ValueError("Justification cannot be empty")
        if training_event.quantity <= 0:
            raise ValueError("Quantity must be a positive integer")
        if training_event.total < 0:
            raise ValueError("Total value cannot be negative")

    def get_training_event_by_id(self, training_event_id: int):
        if not training_event_id > 0:
            raise ValueError("ID must be a positive integer")

        return self.repo.get_training_event_by_id(training_event_id)

    def update_training_event(
        self, training_event_id: int, training_event: TrainingEventSchema
    ) -> TrainingEventResponse:
        activity = self.activity_service.get_activity_by_id(training_event.activity_id)

        self.validate_fields(training_event, activity)
        training_event = self.assign_fields(training_event)

        response = self.repo.update_training_event(training_event_id, training_event)

        logging.info(f"Training event with ID: {training_event_id} updated")

        return response

    def delete_training_event(self, training_event_id: int) -> bool:
        if not training_event_id > 0:
            raise ValueError("ID must be a positive integer")

        success = self.repo.delete_training_event(training_event_id)

        if success:
            logging.info(f"Training events with ID: {training_event_id} deleted")
        else:
            logging.warning(f"Training events with ID: {training_event_id} not found")

        return success
